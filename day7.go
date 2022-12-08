package main

import (
    "bufio"
    "fmt"
    "os"
	"strings"
	"strconv"
	"math"
)

const cutoff_size = 100000
const fs_size = 70000000
const space_required = 30000000

type Node struct {
    name	string
    size	int
	parent	*Node
    children []*Node
}

func checkErr(e error) {
    if e != nil {
        panic(e)
    }
}

func depthFirstAddChildrenIntoSize(node *Node) int {
	fmt.Printf("before %s %d\n", node.name, node.size)
	for _, child := range node.children {
		fmt.Printf("child %s %d\n", child.name, child.size)
		node.size += depthFirstAddChildrenIntoSize(child)
	}
	fmt.Printf("after %s %d\n", node.name, node.size)
	return node.size
}

func depthFirstSumNodesUnderCutoff(node *Node) int {
	result := 0
	fmt.Printf("%s %d\n", node.name, node.size)
	if node.size <= cutoff_size {
		result += node.size
	}

	for _, child := range node.children {
		result += depthFirstSumNodesUnderCutoff(child)
	}
	return result
}

func dfsSmallestNodeAbove(node *Node, space_needed int) int {
	if node.size <= space_needed {
		return math.MaxInt32
	}

	fmt.Printf("%s %d\n", node.name, node.size)

	result := node.size
	for _, child := range node.children {
		child_small := dfsSmallestNodeAbove(child, space_needed)
		fmt.Printf("child %s %d %d\n", child.name, child.size, child_small)

		if child_small < result {
			result = child_small
		}
	}
	return result
}

func main() {
	readFile, err := os.Open("day7.txt")
	checkErr(err)

	var current *Node

    fileScanner := bufio.NewScanner(readFile)
    fileScanner.Split(bufio.ScanLines)

    for fileScanner.Scan() {
		line := fileScanner.Text()
		if strings.HasPrefix(line, "$") {
			switch line {
				case "$ cd /":
					fmt.Println("cd / - root created")
					current = &Node{
						name:  "/",
						size: 0,
						parent: nil,
						children: nil,
					}
					fmt.Println(current)
				case "$ ls":
					continue
				case "$ cd ..":
					current = current.parent
					fmt.Printf("cd .. to: %s\n", current.name)

				default:
					cd_to_child_name := strings.Fields(line)[2]
					for i, child := range current.children {
						fmt.Printf("child: %d %s %d %s\n", i, child.name, child.size, child)
						if child.name == cd_to_child_name {
							current = child

						}
					}
					fmt.Printf("cd to: %s\n", current.name)
			}
		} else if strings.HasPrefix(line, "dir") {
			childName := strings.Fields(line)[1]
			current.children = append(current.children, &Node{
				name: childName,
				size: 0,
				parent: current,
				children: nil,
			})
			fmt.Printf("new child: %s\n", childName)
		} else {
			size, err := strconv.Atoi(strings.Fields(line)[0])
			checkErr(err)
			current.size += size
			fmt.Printf("%s %d\n", current.name, current.size)
		}
    }

    readFile.Close()

	for current.parent != nil {
		current = current.parent
	}

	fmt.Printf("done root: %s %d\n", current.name, current.size)

	depthFirstAddChildrenIntoSize(current)
	fmt.Println("after adding children into size")
	part1Output := depthFirstSumNodesUnderCutoff(current)
	fmt.Printf("part1 output: %d\n", part1Output)

	// part 2
	space_left := fs_size - current.size
	fmt.Printf("space left: %d\n", space_left)
	space_needed := space_required - space_left
	fmt.Printf("space needed: %d\n", space_needed)

	part2Output := dfsSmallestNodeAbove(current, space_needed)
	fmt.Printf("part2 output: %d\n", part2Output)
}