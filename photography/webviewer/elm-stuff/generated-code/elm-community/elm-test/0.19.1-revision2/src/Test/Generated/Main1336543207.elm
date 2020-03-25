module Test.Generated.Main1336543207 exposing (main)

import GroupInfoTest

import Test.Reporter.Reporter exposing (Report(..))
import Console.Text exposing (UseColor(..))
import Test.Runner.Node
import Test

main : Test.Runner.Node.TestProgram
main =
    [     Test.describe "GroupInfoTest" [GroupInfoTest.suite] ]
        |> Test.concat
        |> Test.Runner.Node.run { runs = Nothing, report = (ConsoleReport UseColor), seed = 355556966380400, processes = 4, paths = ["/Users/olivier/Documents/github/visual-experiments/photography/webviewer/tests/Fuzzing.elm","/Users/olivier/Documents/github/visual-experiments/photography/webviewer/tests/GroupInfoTest.elm"]}