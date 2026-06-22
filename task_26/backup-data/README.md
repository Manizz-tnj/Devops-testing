# Task 26 - S3 Backup Solution

## Objective

Implement a backup and restore solution using Amazon S3 for application and configuration files.

## Architecture

Application Files → AWS S3 Bucket → Restore Process

## Steps Performed

1. Created an S3 bucket.
2. Created sample application and configuration files.
3. Uploaded files to S3 using AWS CLI.
4. Verified backup in the S3 bucket.
5. Restored files from S3 to a local directory.
6. Validated restored files.

## Backup Command

```bash
aws s3 cp ./backup-data s3://<bucket-name>/backup/ --recursive
```

## Restore Command

```bash
aws s3 cp s3://<bucket-name>/backup/ ./restore-data --recursive
```

## Validation

```bash
aws s3 ls s3://<bucket-name>/backup/
```

## Outcome

* Successfully backed up files to Amazon S3.
* Successfully restored files from S3.
* Demonstrated a basic disaster recovery and backup strategy using AWS services.
