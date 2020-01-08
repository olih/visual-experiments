module Test.Generated.Main517229127 exposing (main)

import RangeParamsUnitTests

import Test.Reporter.Reporter exposing (Report(..))
import Console.Text exposing (UseColor(..))
import Test.Runner.Node
import Test

main : Test.Runner.Node.TestProgram
main =
    [     Test.describe "RangeParamsUnitTests" [RangeParamsUnitTests.suite] ]
        |> Test.concat
        |> Test.Runner.Node.run { runs = Nothing, report = (ConsoleReport UseColor), seed = 215453824623763, processes = 4, paths = ["/Users/olivier/Documents/github/visual-experiments/brush-ui/tests/Fuzzing.elm","/Users/olivier/Documents/github/visual-experiments/brush-ui/tests/RangeParamsUnitTests.elm"]}