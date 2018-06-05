package main

import (
	"crypto/hmac"
	"crypto/sha1"
	"encoding/base64"
	"errors"
	"fmt"
	"sort"
	"strings"
)

const (
	AccessKey = "ThisIsAccessKey"
	SecretKey = "ThisIsSecretKey"
)

func main() {
	method := "POST"
	headers := map[string]string{
		"Date":            "Mon, 01 Jan 2018 08:08:08 GMT",
		"Content-Sha1":     "123abc",
		"Content-Type":    "application/json",
		"dragonex-btruth": "DragonExIsTheBest2",
		"Dragonex-Atruth": "DragonExIsTheBest",
	}
	resource := "/api/v1/token/new/"
	sign(SecretKey, method, headers, resource)

}

var (
	SignError = errors.New("sign error")
)

func sign(secretKey, method string, headers map[string]string, resource string) (string, error) {
	newHeaders := map[string]string{}
	for k, v := range headers {
		newHeaders[strings.ToLower(k)] = v
	}

	contentSha1 := newHeaders["content-sha1"]
	contentType := newHeaders["content-type"]
	date := newHeaders["date"]

	dragonHeaders := make([]string, 0, len(newHeaders))
	canonicalizedDragonExHeaders := ""
	for k, v := range newHeaders {
		if strings.HasPrefix(k, "dragonex-") {
			dragonHeaders = append(dragonHeaders, fmt.Sprintf("%s:%s", k, v))
		}
	}
	sort.Strings(dragonHeaders)
	if len(dragonHeaders) != 0 {
		canonicalizedDragonExHeaders = strings.Join(dragonHeaders, "\n")
		canonicalizedDragonExHeaders += "\n"
	}

	stringsToSignSlice := []string{
		strings.ToUpper(method),
		contentSha1,
		contentType,
		date,
		canonicalizedDragonExHeaders,
	}
	stringToSign := strings.Join(stringsToSignSlice, "\n")
	stringToSign += resource

	sha1Hash := hmac.New(sha1.New, []byte(secretKey))
	if _, e := sha1Hash.Write([]byte(stringToSign)); e != nil {
		return "", SignError
	}

	signature := base64.StdEncoding.EncodeToString(sha1Hash.Sum(nil))

	println(fmt.Sprintf("stringToSign=%s\nsign=%s", stringToSign, signature))
	return signature, nil
}
