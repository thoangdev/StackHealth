# Security Reports

This directory contains automated security scan results for the StackHealth application.

## Generated Reports

### Trivy Vulnerability Scanner
- **File**: `trivy-results.json`
- **Purpose**: Filesystem vulnerability scanning
- **What it scans**: Dependencies, container images, and filesystem for known vulnerabilities
- **Format**: JSON with detailed vulnerability information including CVE IDs, severity levels, and fix recommendations

### Bandit Security Linter
- **File**: `bandit-report.json` 
- **Purpose**: Python code security analysis
- **What it scans**: Python source code for common security issues
- **Detects**: SQL injection, hardcoded passwords, shell injection, insecure random generators, etc.

### Safety Dependency Check
- **File**: `safety-report.json`
- **Purpose**: Python dependency vulnerability check
- **What it scans**: Python packages in requirements.txt for known security vulnerabilities
- **Database**: Uses PyUp.io vulnerability database

### Summary Report
- **File**: `security-summary.md`
- **Purpose**: Human-readable summary of all security scans
- **Contents**: Overview of findings, file sizes, and recommended next steps

### Scan Metadata
- **File**: `last-scan.txt`
- **Purpose**: Timestamp of the last security scan execution

## Scan Schedule

Security scans run automatically:
- ✅ **Every Monday at 2 AM UTC** (weekly scheduled scan)
- ✅ **On every push to main branch**
- ✅ **On every pull request to main branch**

## Understanding the Results

### Severity Levels
- **Critical**: Immediate action required
- **High**: Should be fixed soon
- **Medium**: Should be reviewed and fixed when possible
- **Low**: Nice to fix, but not urgent
- **Info**: Informational findings

### Common Issues to Look For

#### Trivy Results
- Outdated dependencies with known CVEs
- Base image vulnerabilities (if using containers)
- Package manager vulnerabilities

#### Bandit Results
- Hardcoded secrets or passwords
- Use of insecure functions (eval, exec, etc.)
- SQL injection vulnerabilities
- Insecure random number generation
- Shell injection risks

#### Safety Results
- Python packages with known security vulnerabilities
- Deprecated packages with security issues
- Packages with malicious code

## Taking Action

### High Priority Actions
1. **Review Critical and High severity findings immediately**
2. **Update vulnerable dependencies** to patched versions
3. **Fix code-level security issues** identified by Bandit
4. **Replace insecure functions** with secure alternatives

### Medium Priority Actions
1. Review Medium severity findings
2. Plan updates for affected dependencies
3. Consider security improvements for flagged code patterns

### Monitoring
1. Check scan results after each push
2. Monitor for new vulnerabilities in existing dependencies
3. Set up alerts for critical/high severity findings

## Manual Security Scanning

You can run security scans locally before pushing:

```bash
# Test all security tools
make test-security

# Install security tools manually
pip3 install bandit safety
# For Trivy: https://aquasecurity.github.io/trivy/

# Run individual scans
bandit -r backend/                    # Code security
safety check                         # Dependency check
trivy fs .                           # Filesystem scan
```

## Exclusions and False Positives

If you need to exclude certain findings:

### Bandit
Create a `.bandit` file in the repository root:
```yaml
skips: ['B101', 'B601']  # Skip specific test IDs
exclude_dirs: ['tests']   # Exclude directories
```

### Safety
Use `--ignore` flag for specific vulnerabilities:
```bash
safety check --ignore 12345
```

### Trivy
Create a `.trivyignore` file:
```
CVE-2021-12345
CVE-2020-67890
```

## Integration with CI/CD

The security scans are integrated into the development workflow:

1. **Pre-commit**: Consider adding security checks to pre-commit hooks
2. **Pull Requests**: Security scans run on every PR
3. **Deployment**: Only deploy if security scans pass
4. **Monitoring**: Regular scans catch new vulnerabilities

## Compliance and Reporting

These scans help with:
- **Security compliance** requirements
- **Vulnerability management** processes
- **Risk assessment** for deployments
- **Security audit** preparation

## Resources

- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Safety Documentation](https://pyup.io/safety/)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)

## Questions or Issues?

If you have questions about security findings or need help fixing vulnerabilities:

1. Check the documentation links above
2. Consult the security team
3. Review OWASP guidelines for secure coding
4. Consider security training for the development team
