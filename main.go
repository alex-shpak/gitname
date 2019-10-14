package main

import (
	"bufio"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"os/exec"
	"regexp"
	"strings"
)

var ( // flags
	remoteName string
	quiet      bool
)

func init() {
	flag.StringVar(&remoteName, "remote", "origin", "Specify git remote, defaults to 'origin'")
	flag.BoolVar(&quiet, "q", false, "Quiet mode")
	flag.Parse()

	if quiet { // Mute logging
		log.SetOutput(ioutil.Discard)
	}
}

func main() {
	_, err := exec.LookPath("git")
	if err != nil {
		log.Fatalln(err)
	}

	if output, err := exec.Command("git", "status").CombinedOutput(); err != nil {
		log.Fatal(string(output))
	}

	remote, err := exec.Command("git", "remote", "get-url", remoteName).Output()
	if err != nil {
		log.Fatalf("Remote '%s' not found", highlight(remoteName))
	}

	urlParts := urlParts(string(remote))
	config := map[string]string{}

	// Merge config values, more deep links have higher force
	for n := range urlParts {
		subsection := strings.Join(urlParts[:n], "/")
		values := gitSubsectionConfig(subsection)

		for k, v := range values {
			config[k] = v
		}
	}

	// Set resolved config values
	for name, value := range config {
		if err := exec.Command("git", "config", name, value).Run(); err != nil {
			log.Fatalln(err)
		}
	}

	status()
}

// urlParts returns essential parts of git remote. Removes schema, auth and splitting into parts.
func urlParts(url string) []string {
	substrAfter := func(s string, sub string) string {
		from := strings.Index(url, sub) + len(sub)
		return s[from:]
	}

	url = strings.TrimSpace(url)
	url = substrAfter(url, "://")
	url = substrAfter(url, "@")

	return regexp.MustCompile("[:/@]+").Split(url, -1)
}

// gitSubsectionConfig picks config params filtered by subsection, errors are ignored. Returns key-values pairs or an empty map
func gitSubsectionConfig(subsection string) (values map[string]string) {
	values = map[string]string{}
	section := fmt.Sprintf(".*\\.%s\\.", subsection)

	bytes, err := exec.Command("git", "config", "--global", "--get-regexp", section).Output()
	if err != nil {
		return
	}

	scanner := bufio.NewScanner(
		strings.NewReader(string(bytes)),
	)

	for scanner.Scan() {
		kv := strings.SplitN(scanner.Text(), " ", 2) // Split into key and value

		// Remove subsection from key
		key := strings.Replace(kv[0], ("." + subsection), "", 1)
		value := kv[1]

		values[key] = value
	}

	return
}

// status prints git commiter name and email
func status() {
	name, _ := exec.Command("git", "config", "-z", "user.name").Output()
	email, _ := exec.Command("git", "config", "-z", "user.email").Output()

	author := fmt.Sprintf("%s <%s>", string(name), string(email))
	log.Printf("Committing as %s", highlight(author))
}

// highlight returns text wrapped in ANSI coloring
func highlight(text string) string {
	return fmt.Sprintf("\033[0;32m%s\033[0m", text)
}
