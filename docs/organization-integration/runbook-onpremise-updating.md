# Runbook: Sigrid On-Premise Updating

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

This documentation offers useful context on how to keep on-premise Sigrid up-to-date, making it an excellent starting point for ongoing maintenance.

## Prerequisites

- You should have already read the other Sigrid On-Premise documentation
- You have a running Sigrid Deployment
- You have access to Software Improvement Group AWS ECR registry

## Update Frequency

We update container images daily for immediate improvements. The Helm chart is updated less frequently, only when new features or significant changes are released. This ensures you get rapid updates while maintaining chart stability.

- Sigrid Docker containers: Monthly at minimum, ideally with each release.
- Sigrid Helm chart: Quarterly, preferred bi-weekly, ideally whenever a new version is available.

## Update Instructions

1. Update Helm Chart
2. Update Container
3. Update ImageTag
4. Apply the updates using Helm

### Update Containers

- Situation 1: Using your own container registry, see [Detailed instructions for accessing and using SIG's AWS ECR](onpremise-aws-ecr.md).
  - Pull the latest Docker containers.
- Situation 2: Pulling images directly from SIG's AWS ECR Registry.
  - When this is already set up, you don't need to take any action for this step.

### Update image tag (Sigrid version)

Update the `imageTag` in the `global` section of the Helm chart's values file (usually `custom-values.yaml`):

```bash
   global:
     ImageTag: "<REPLACE-WITH-LATEST-VERSION>"
```

### Apply the updates using Helm

To apply the updates using Helm, you can use the following command. Note how to do this might vary depending on how you deployed Sigrid.

```bash
   helm upgrade --install sigrid-onprem ./sigrid-stack -n sigrid --values ./sigrid-stack/custom-values.yaml
```

## Test Instructions

1. After updating, verify that all pods are running:
2. Check the logs of key services for any errors
3. Access the Sigrid frontend and perform basic operations to ensure functionality.
4. Run a test analysis on a sample project to verify the entire pipeline is working correctly.
If any issues are encountered during testing, consider rolling back to the previous version and contacting support.

## Additional System Maintenance

In addition to updating Sigrid components, it's important to maintain other systems that Sigrid depends on:

- PostgreSQL: Ensure that your PostgreSQL database is regularly updated and maintained. Keep the PostgreSQL version within the latest two supported major versions.
- Other (e.g., GitLab): Regularly update and maintain your supporting systems.

The update frequency for these systems should be determined based on your organization's needs and policies. However, it's crucial to keep these systems up-to-date to ensure optimal performance, security, and compatibility with Sigrid.

Note: Specific update instructions for PostgreSQL and and other systems are not provided here, as they can vary depending on your setup and chosen systems. Please refer to the official documentation of these systems for proper update procedures.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.
