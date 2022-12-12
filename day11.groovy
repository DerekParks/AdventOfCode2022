import groovy.transform.ToString 

class Global {
    static boolean is_part1 = false
    static boolean is_debug = false
    static int part2_divisor = -1
}

@ToString(includeNames=true)
class Monkey {
    def items = []
    int testDivByOpt = -1
    int mulNext = 1
    int addNext = 0
    boolean isOld = false
    int trueThrowTo = 0
    int falseThrowTo = 0
    long inspectCount = 0
    def evalNextItem() {
        inspectCount++
        def nextItem = items.first()
        items = items.tail()

        long nextItemValue = isOld ? nextItem * nextItem : nextItem * mulNext + addNext
        long nextItemValueAfterDiv = Global.is_part1 ? (nextItemValue / 3).toLong() : (nextItemValue % Global.part2_divisor).toLong()

        if(Global.is_debug) {
            println "nextItem: ${nextItem}"
            println "nextItemValue: ${nextItemValue}"
            println "nextItemValueAfterDiv: ${nextItemValueAfterDiv}"
        }

        return nextItemValueAfterDiv % testDivByOpt == 0? [nextItemValueAfterDiv, trueThrowTo] : [nextItemValueAfterDiv, falseThrowTo]
    }
}

String fileContents = new File('day11.txt').getText('UTF-8')

def pattern = /Monkey\s(\d):(\s+)Starting items:(\s+)([\d,\s]+)+\sOperation: new = old ([*+]) ([old\d]+)\s+Test: divisible by\s(\d+)\s+If true: throw to monkey (\d)\s+If false: throw to monkey (\d)\s+/
def matches = (fileContents =~ pattern).findAll()

def monkeys = []

def divisors = []

for (match in matches) {
    int monkeyIndex = match[1].toInteger()
    def items = match[4].split(',').collect { it.toLong() }
    String operation = match[5]
    String operand = match[6]
    int testDivBy = match[7].toInteger()
    int trueThrowTo = match[8].toInteger()
    int falseThrowTo = match[9].toInteger()

    boolean isOld = operand == 'old'
    int mulNext = !isOld && operation == '*' ? operand.toInteger() : 1
    int addNext = !isOld && operation == '+' ? operand.toInteger() : 0

    monkeys.add(new Monkey(
        items: items, 
        testDivByOpt: testDivBy,
        isOld: isOld,
        mulNext: mulNext,
        addNext: addNext,
        trueThrowTo: trueThrowTo,
        falseThrowTo: falseThrowTo)
    )

    divisors.add(testDivBy)

    assert monkeys.size() == monkeyIndex + 1
}

def lcm(listOfDivisors) {
    long m = listOfDivisors.max()
    while(true) {
       if(listOfDivisors.every { m % it == 0 })
           break
       m += 1
    }
   return m
}

if (!Global.is_part1) {
    Global.part2_divisor = lcm(divisors)
    println "Part 2 divisor: ${Global.part2_divisor}"
}

int nRounds = Global.is_part1 ? 20 : 10000

for (int round=0; round < nRounds; round++) {
    println "Round: ${round + 1}"

    for (monkey in monkeys) {
        while (monkey.items.size() > 0) {

            def reuslt = monkey.evalNextItem()
            def nextItem = reuslt[0]
            def toMonkey = reuslt[1]
            //println "$nextItem, $toMonkey"

            monkeys[toMonkey].items << nextItem
            //println monkeys[toMonkey].items
        }
    }
}

for (int i=0; i < monkeys.size(); i++) {
    println "${i}  ${monkeys[i].inspectCount}"
}

monkeys.sort { 
    it.inspectCount
}

println monkeys[-1].inspectCount * monkeys[-2].inspectCount