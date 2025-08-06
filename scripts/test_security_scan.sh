#!/bin/bash
# Test security scanning tools locally
# This script helps validate the security workflow before pushing to GitHub

set -e  # Exit on any error

echo "🔒 Testing Security Scanning Tools"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    echo "❌ Error: Run this script from the root of the stackhealth repository"
    exit 1
fi

# Check if tools are available
echo "🔍 Checking security tools availability..."

# Check Bandit
if command -v bandit >/dev/null 2>&1; then
    echo "✅ Bandit is installed"
    BANDIT_AVAILABLE=true
else
    echo "❌ Bandit not found. Install with: pip3 install bandit"
    BANDIT_AVAILABLE=false
fi

# Check Safety
if command -v safety >/dev/null 2>&1; then
    echo "✅ Safety is installed"
    SAFETY_AVAILABLE=true
else
    echo "❌ Safety not found. Install with: pip3 install safety"
    SAFETY_AVAILABLE=false
fi

# Check Trivy
if command -v trivy >/dev/null 2>&1; then
    echo "✅ Trivy is installed"
    TRIVY_AVAILABLE=true
else
    echo "❌ Trivy not found. Install from: https://aquasecurity.github.io/trivy/"
    TRIVY_AVAILABLE=false
fi

echo ""

# Install missing tools if requested
if [ "$BANDIT_AVAILABLE" = false ] || [ "$SAFETY_AVAILABLE" = false ]; then
    echo "🔧 Installing missing Python security tools..."
    pip3 install bandit safety
    echo "✅ Python security tools installed"
    echo ""
fi

# Run Bandit scan
if [ "$BANDIT_AVAILABLE" = true ] || command -v bandit >/dev/null 2>&1; then
    echo "🔍 Running Bandit security scan on backend code..."
    bandit -r backend/ -f json -o test-bandit-report.json || true
    echo "📋 Bandit scan summary:"
    bandit -r backend/ || true
    echo "✅ Bandit scan completed"
    echo ""
else
    echo "⚠️  Skipping Bandit scan (not available)"
    echo ""
fi

# Run Safety check
if [ "$SAFETY_AVAILABLE" = true ] || command -v safety >/dev/null 2>&1; then
    echo "🔍 Running Safety dependency check..."
    cd backend
    safety check --json --output ../test-safety-report.json || true
    echo "📋 Safety scan summary:"
    safety check || true
    cd ..
    echo "✅ Safety scan completed"
    echo ""
else
    echo "⚠️  Skipping Safety scan (not available)"
    echo ""
fi

# Run Trivy scan (if available)
if [ "$TRIVY_AVAILABLE" = true ]; then
    echo "🔍 Running Trivy filesystem scan..."
    trivy fs --format json --output test-trivy-results.json . || true
    echo "📋 Trivy scan summary:"
    trivy fs --format table . || true
    echo "✅ Trivy scan completed"
    echo ""
else
    echo "⚠️  Skipping Trivy scan (not available)"
    echo "💡 To install Trivy on macOS: brew install trivy"
    echo "💡 To install Trivy on Ubuntu: https://aquasecurity.github.io/trivy/v0.18.3/installation/"
    echo ""
fi

# Create test summary
echo "📋 Creating security test summary..."
cat > test-security-summary.md << EOF
# Security Scan Test Results

Generated on: $(date)

## Tools Tested

- **Bandit**: $(if [ -f test-bandit-report.json ]; then echo "✅ Completed"; else echo "❌ Not run"; fi)
- **Safety**: $(if [ -f test-safety-report.json ]; then echo "✅ Completed"; else echo "❌ Not run"; fi)
- **Trivy**: $(if [ -f test-trivy-results.json ]; then echo "✅ Completed"; else echo "❌ Not run"; fi)

## Generated Files

EOF

if [ -f test-bandit-report.json ]; then
    BANDIT_SIZE=$(wc -c < test-bandit-report.json)
    echo "- \`test-bandit-report.json\` - ${BANDIT_SIZE} bytes" >> test-security-summary.md
fi

if [ -f test-safety-report.json ]; then
    SAFETY_SIZE=$(wc -c < test-safety-report.json)
    echo "- \`test-safety-report.json\` - ${SAFETY_SIZE} bytes" >> test-security-summary.md
fi

if [ -f test-trivy-results.json ]; then
    TRIVY_SIZE=$(wc -c < test-trivy-results.json)
    echo "- \`test-trivy-results.json\` - ${TRIVY_SIZE} bytes" >> test-security-summary.md
fi

echo "" >> test-security-summary.md
echo "## Next Steps" >> test-security-summary.md
echo "" >> test-security-summary.md
echo "1. Review the generated report files for security issues" >> test-security-summary.md
echo "2. Fix any identified vulnerabilities before deploying" >> test-security-summary.md
echo "3. The GitHub Actions workflow will run these same scans automatically" >> test-security-summary.md

# Display summary
echo "📊 Security Test Summary"
echo "======================="
cat test-security-summary.md

echo ""
echo "📁 Generated test files:"
ls -la test-*-report.json test-*-results.json test-security-summary.md 2>/dev/null || echo "No test files generated"

echo ""
echo "🧹 Cleaning up test files..."
rm -f test-bandit-report.json test-safety-report.json test-trivy-results.json test-security-summary.md

echo "✅ Security scan test completed!"
echo ""
echo "💡 The GitHub Actions security workflow is ready to run with these tools."
echo "🔒 Push your code to trigger the automated security scanning."
