Author: Joshua Bognar

Script for summarising Shimadzu Mobile Dart EXI logs.

Tested on MX7, MX8

Takes as input a directory containing .csv files of raw EXI log exports. This directory must not contain any other .csv files.

Saved output contains number of examinations and median data for each examination of:
  - kV
  - mAs
  - DAP
  - EXI
  - Collimation
  - SID
  - Target dose
