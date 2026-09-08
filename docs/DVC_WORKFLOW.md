# DVC Workflow

## Purpose

DVC (Data Version Control) is used to track and version datasets alongside Git. Git tracks the DVC metadata files, while DVC stores the actual dataset files.

## Local DVC Remote

The project uses a local DVC remote:

`~/dvc-remote-storage`

It is configured as the default remote named `myremote`.

## Dataset Versioning Workflow

The workflow used in this project is:

`dvc add → git add → git commit → dvc push`

### Version 1

The original Iris dataset contains 150 data rows.

Git commit:

`a6081fa data: add iris_v1 raw dataset (150 rows) tracked via DVC`

### Version 2

20 synthetic rows were added, increasing the dataset from 150 to 170 rows.

Git commit:

`490ccb2 data: augment iris dataset with 20 synthetic rows (150 -> 170)`

The updated dataset was pushed to the DVC remote using:

`dvc push`

## Comparing Dataset Versions

The command:

`dvc diff a6081fa`

showed that:

`data/raw/iris_v1.csv`

was modified.

## Reproducing Historical Data

A historical dataset version can be restored using:

`git checkout <commit> -- data/raw/iris_v1.csv.dvc`

followed by:

`dvc checkout data/raw/iris_v1.csv.dvc`

Version 1 was successfully restored to 150 rows, and Version 2 was restored to 170 rows.

## Conclusion

DVC provides dataset versioning and reproducibility by keeping large data files outside normal Git tracking while Git records the dataset versions through DVC metadata files.