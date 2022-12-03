object RPS extends Enumeration {
    type RPS = Value
    val Paper = Value("Paper")
    val Scissors = Value("Scissors")
    val Rock = Value("Rock")
}

object WLD extends Enumeration {
    type WLD = Value
    val Win = Value("Win")
    val Lose = Value("Lose")
    val Draw = Value("Draw")
}

object Day2 {
    import RPS._
    import WLD._
    def toRPS(s: String): RPS = s match {
        case "A" | "X" => Rock
        case "B" | "Y" => Paper
        case "C" | "Z" => Scissors
        case _ => throw new IllegalArgumentException("Invalid input")
    }

    def toWLD(s: String): WLD = s match {
        case "X" => Lose
        case "Y" => Draw
        case "Z" => Win
        case _ => throw new IllegalArgumentException("Invalid input")
    }

    def winPts(theirs: RPS, ours: RPS): Int = (theirs, ours) match {
        case (Rock, Paper) | (Paper, Scissors) | (Scissors, Rock) => 6
        case (Rock, Rock)  | (Paper, Paper)    | (Scissors, Scissors) => 3
        case _ => 0
    }

    def shapePts(ours: RPS): Int = ours match {
        case Rock => 1
        case Paper => 2
        case Scissors => 3
        case _ => throw new IllegalArgumentException("Invalid input")
    }

    def score(theirs: RPS, ours: RPS): Int = winPts(theirs, ours) + shapePts(ours)

    def whatShouldIThrow(theirs: RPS, wld: WLD): RPS = (theirs, wld) match {
        case (Rock, Win) => Paper
        case (Rock, Lose) => Scissors
        case (Rock, Draw) => Rock
        case (Paper, Win) => Scissors
        case (Paper, Lose) => Rock
        case (Paper, Draw) => Paper
        case (Scissors, Win) => Rock
        case (Scissors, Lose) => Paper
        case (Scissors, Draw) => Scissors
        case _ => throw new IllegalArgumentException("Invalid input")
    }

    def part1(input : Seq[String]): Int = {
        val scores = input.map(_.split(" ").map(toRPS)).map(x => score(x(0), x(1)))
        scores.sum
    }

    def part2(input : Seq[String]): Int = {
        val scores = input.map(_.split(" ")).map(x => {
            val theirs = toRPS(x(0))
            val wld = toWLD(x(1))
            val ours = whatShouldIThrow(theirs, wld)
            score(theirs, ours)
        })
        scores.sum
    }

    def main(args: Array[String]): Unit = {
        val input = scala.io.Source.fromFile("day2.txt").getLines.toSeq
        println(part1(input))
        println(part2(input))
    }

}