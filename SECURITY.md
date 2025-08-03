# Security Policy

## Supported Versions

We actively support and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| 1.x.x   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in StackHealth Scorecard Platform, please report it responsibly.

### How to Report

1. **Email**: Send details to hoangtommyquoc@gmail.com
2. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment**: Within 24 hours
- **Initial Assessment**: Within 72 hours
- **Regular Updates**: Every 7 days until resolved
- **Resolution Timeline**: Critical issues within 30 days

### Security Best Practices

#### For Administrators

- Change default credentials immediately
- Use strong, unique passwords
- Enable two-factor authentication when available
- Regularly update to the latest version
- Monitor access logs
- Use HTTPS in production
- Implement proper network security

#### For Developers

- Follow secure coding practices
- Validate all input data
- Use parameterized queries
- Implement proper error handling
- Keep dependencies updated
- Use environment variables for secrets
- Regular security testing

### Vulnerability Disclosure Timeline

1. **Day 0**: Vulnerability reported
2. **Day 1**: Acknowledgment sent
3. **Day 3**: Initial assessment completed
4. **Day 7**: Fix development begins
5. **Day 30**: Security update released
6. **Day 90**: Public disclosure (if appropriate)

### Bug Bounty Program

We currently operate a private bug bounty program. Contact security@stackhealth.com for details on participation.

### Security Features

- JWT-based authentication
- Password hashing with bcrypt
- SQL injection protection
- XSS prevention
- CSRF protection
- Rate limiting
- Input validation
- Secure file handling
- Environment-based configuration
