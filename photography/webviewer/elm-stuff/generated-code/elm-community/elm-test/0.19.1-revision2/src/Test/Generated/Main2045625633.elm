module Test.Generated.Main2045625633 exposing (main)

import Example

import Test.Reporter.Reporter exposing (Report(..))
import Console.Text exposing (UseColor(..))
import Test.Runner.Node
import Test

main : Test.Runner.Node.TestProgram
main =
    [     Test.describe "Example" [Example.suite] ]
        |> Test.concat
        |> Test.Runner.Node.run { runs = Nothing, report = (ConsoleReport UseColor), seed = 117149689720305, processes = 4, paths = ["/Users/olivier/Documents/github/visual-experiments/photography/webviewer/tests/Example.elm"]}