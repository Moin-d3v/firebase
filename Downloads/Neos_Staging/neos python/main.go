package main

import (
	"bufio"
	"bytes"
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/base64"
	"encoding/binary"
	"encoding/pem"
	"flag"
	"fmt"
	"log"
	"math/big"
	"os"
	"strings"
	"time"

	"github.com/dgrijalva/jwt-go"
)

// {
//     "admin_user_id": "d16a353b-0585-455f-9a00-4a8c9b89db54",
//     "device_id": "oFVOMMMeOplkecf7yE7s"
// }

var (
	testUserId = "1e00dae9-3b5d-40cd-811c-8ddbb1f55281" // Arbitrary static ID
	testNeosId = "2OuYa8HQQbe50cWt1jpc"                 // Arbitrary static ID
)

type hasRoleTestInput struct {
	signedRawUrlSafeB64Jwt             string
	scopesRequiredForEndpointSetByYAML []string
}

var testPrivateKey *rsa.PrivateKey
var testPublicKey *rsa.PublicKey

func init() {
	// testPrivateKey, testPublicKey = GenerateKeyPair(2048)

	// savePrivateKeyToPem(testPrivateKey)

	testPrivateKey, testPublicKey = loadKeyPairFromPem()
	byteE := newBufferFromInt(uint64(testPublicKey.E))
	exS := base64URLEncode(byteE)
	modS := base64URLEncode(testPublicKey.N.Bytes())

	// log.Println("Exponent String")
	// log.Println(exS)
	// log.Println("Modulus String")
	// log.Println(modS)
	GeneratePublicRSAKeyUsingB64Input(&modS, &exS)
}

func savePrivateKeyToPem(privateKey *rsa.PrivateKey) {
	pemPrivateFile, err := os.Create("private_key.pem")
	if err != nil {
		fmt.Println("Error creating pem file: %s", err)
		os.Exit(1)
	}

	var pemPrivateBlock = &pem.Block{
		Type:  "RSA PRIVATE KEY",
		Bytes: x509.MarshalPKCS1PrivateKey(privateKey),
	}

	err = pem.Encode(pemPrivateFile, pemPrivateBlock)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	pemPrivateFile.Close()
}

func loadKeyPairFromPem() (*rsa.PrivateKey, *rsa.PublicKey) {
	privateKeyFile, err := os.Open("private_key.pem")
	if err != nil {
		fmt.Println("Error opening pem file: %s", err)
		os.Exit(1)
	}

	pemfileinfo, _ := privateKeyFile.Stat()
	var size int64 = pemfileinfo.Size()
	pembytes := make([]byte, size)
	buffer := bufio.NewReader(privateKeyFile)
	_, err = buffer.Read(pembytes)
	data, _ := pem.Decode([]byte(pembytes))
	privateKeyFile.Close()

	privateKeyImported, err := x509.ParsePKCS1PrivateKey(data.Bytes)
	if err != nil {
		fmt.Println("Error reading pem file: %s", err)
		os.Exit(1)
	}
	return privateKeyImported, &privateKeyImported.PublicKey
}

type neoneJWTPayload struct {
	Scope string `json:"scope"` // space separated list of individual scopes to request.
	jwt.StandardClaims
}

// Helper function that takes a space separated scope list and returns a generated JWT
func createJwtWithScope(scope string) (generatedJWT *jwt.Token) {
	log.Println("&testUserId: ", testUserId)
	log.Println("&testNeosId: ", testNeosId)

	claims := &neoneJWTPayload{
		Scope: scope,
		StandardClaims: jwt.StandardClaims{
			Subject:   testUserId,
			ExpiresAt: time.Now().Add(5000 * time.Minute).Unix(),
			IssuedAt:  time.Now().Add(-5 * time.Minute).Unix(), // NOTE SUBTRACTION BY ADDITION OF NEGATIVE
		},
	}

	generatedJWT = jwt.NewWithClaims(jwt.SigningMethodRS256, claims)
	return
}

// GenerateKeyPair generates a new key pair
func GenerateKeyPair(bits int) (*rsa.PrivateKey, *rsa.PublicKey) {
	privkey, err := rsa.GenerateKey(rand.Reader, bits)
	if err != nil {
		log.Printf("Failed to generate RSA Keypair with error: %s\n", err)
	}
	return privkey, &privkey.PublicKey
}

func main() {
	jwtTest_EmptyScope := createJwtWithScope("post_write")
	jwtTest_EmptyScope.Header["kid"] = testNeosId
	signedJWT, err := jwtTest_EmptyScope.SignedString(testPrivateKey)
	if err != nil {
		log.Printf("Test failed: Unable to sign JWT for test input. Got error: %s\n", err)
		return
	}

	fmt.Printf("%s", signedJWT)

}

// byteBuffer represents a slice of bytes that can be serialized to url-safe base64.
type byteBuffer struct {
	data []byte
}

// Url-safe base64 encode that strips padding
func base64URLEncode(data []byte) string {
	var result = base64.URLEncoding.EncodeToString(data)
	return strings.TrimRight(result, "=")
}

func newBufferFromInt(num uint64) []byte {
	data := make([]byte, 8)
	binary.BigEndian.PutUint64(data, num)
	return bytes.TrimLeft(data, "\x00")
}

func GetExponentInt(exponent string) int {
	eStr := exponent
	decE, err := base64.RawURLEncoding.DecodeString(eStr)
	if err != nil {
		return int(0)
	}
	var eBytes []byte
	if len(decE) < 8 {
		eBytes = make([]byte, 8-len(decE), 8)
		eBytes = append(eBytes, decE...)
	} else {
		eBytes = decE
	}
	eReader := bytes.NewReader(eBytes)
	var e uint64
	err = binary.Read(eReader, binary.BigEndian, &e)
	if err != nil {
		return int(0)
	}
	return int(e)
}

func GeneratePublicRSAKeyUsingB64Input(modulus *string, exponent *string) {
	nStr := *modulus
	decN, err := base64.RawURLEncoding.DecodeString(nStr)
	if err != nil {
		log.Println(err.Error())
	}
	n := big.NewInt(0)
	n.SetBytes(decN)

	eStr := *exponent
	decE, err := base64.RawURLEncoding.DecodeString(eStr)
	if err != nil {
		log.Println(err.Error())
	}
	var eBytes []byte
	if len(decE) < 8 {
		eBytes = make([]byte, 8-len(decE), 8)
		eBytes = append(eBytes, decE...)
	} else {
		eBytes = decE
	}
	eReader := bytes.NewReader(eBytes)
	var e uint64
	err = binary.Read(eReader, binary.BigEndian, &e)
	if err != nil {
		log.Println(err.Error())
	}

}

func init() {

	flag.StringVar(&testUserId, "user-id", "", "string var")
	flag.StringVar(&testNeosId, "device-token", "", "string var")

	flag.Parse()

}
