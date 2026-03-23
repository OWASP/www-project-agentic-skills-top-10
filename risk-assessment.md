---
layout: col-sidebar
title: Interactive Risk Assessment Tool
tags: risk-assessment, security-tool, interactive
level: 2
type: documentation
pitch: Assess your AI agent skills for security risks
description: "Interactive tool to evaluate AI agent skills against the OWASP AST10 security risks and generate personalized mitigation recommendations."
---

# Interactive Risk Assessment Tool

Use this tool to assess your AI agent skills for security vulnerabilities based on the OWASP Agentic Skills Top 10 (AST10) framework.

<div id="assessment-container">
  <div id="progress-bar">
    <div id="progress-fill"></div>
    <span id="progress-text">Question 1 of 10</span>
  </div>

  <div id="question-container">
    <h3 id="question-title">Loading assessment...</h3>
    <p id="question-description"></p>
    <div id="options-container"></div>
  </div>

  <div id="navigation">
    <button id="prev-btn" disabled>Previous</button>
    <button id="next-btn">Next</button>
  </div>
</div>

<div id="results-container" style="display: none;">
  <h2>Risk Assessment Results</h2>
  <div id="risk-score">
    <h3>Overall Risk Score: <span id="score-value"></span></h3>
    <div id="score-bar">
      <div id="score-fill"></div>
    </div>
  </div>

  <div id="risk-breakdown">
    <h3>Risk Breakdown</h3>
    <div id="risk-items"></div>
  </div>

  <div id="recommendations">
    <h3>Recommended Mitigations</h3>
    <div id="mitigation-list"></div>
  </div>

  <div id="action-buttons">
    <button id="download-report">Download Report</button>
    <button id="retake-assessment">Retake Assessment</button>
  </div>
</div>

<script>
// AST10 Assessment Questions
const questions = [
  {
    id: 'ast01',
    title: 'AST01 - Malicious Skills',
    description: 'Does your skill request or execute potentially dangerous operations?',
    options: [
      { text: 'No, my skill only performs safe, read-only operations', value: 0 },
      { text: 'My skill requests some permissions but validates all inputs', value: 1 },
      { text: 'My skill executes shell commands or modifies system files', value: 3 },
      { text: 'My skill downloads external content or connects to unknown servers', value: 4 }
    ]
  },
  {
    id: 'ast02',
    title: 'AST02 - Supply Chain Compromise',
    description: 'How does your skill handle dependencies and external resources?',
    options: [
      { text: 'No external dependencies or resources', value: 0 },
      { text: 'Uses well-known, verified libraries with pinned versions', value: 1 },
      { text: 'Uses some external resources but validates them', value: 2 },
      { text: 'Downloads unverified content or uses unpinned dependencies', value: 4 }
    ]
  },
  {
    id: 'ast03',
    title: 'AST03 - Over-Privileged Skills',
    description: 'What permissions does your skill require?',
    options: [
      { text: 'Minimal permissions (read-only access to specific files)', value: 0 },
      { text: 'Moderate permissions with clear justification', value: 1 },
      { text: 'Broad permissions (full filesystem access, network access)', value: 3 },
      { text: 'Excessive permissions without clear need', value: 4 }
    ]
  },
  {
    id: 'ast04',
    title: 'AST04 - Insecure Metadata',
    description: 'How accurate and secure is your skill\'s metadata?',
    options: [
      { text: 'Complete, accurate metadata with verified publisher info', value: 0 },
      { text: 'Mostly accurate but some missing information', value: 1 },
      { text: 'Inaccurate descriptions or misleading information', value: 3 },
      { text: 'No metadata or completely misleading information', value: 4 }
    ]
  },
  {
    id: 'ast05',
    title: 'AST05 - Insufficient Input Validation',
    description: 'How does your skill handle user inputs?',
    options: [
      { text: 'All inputs are validated and sanitized', value: 0 },
      { text: 'Most inputs validated, some edge cases covered', value: 1 },
      { text: 'Basic validation but some inputs could be exploited', value: 2 },
      { text: 'No input validation or weak validation', value: 4 }
    ]
  },
  {
    id: 'ast06',
    title: 'AST06 - Improper Error Handling',
    description: 'How does your skill handle errors and exceptions?',
    options: [
      { text: 'Comprehensive error handling with secure failure modes', value: 0 },
      { text: 'Good error handling but some information leakage possible', value: 1 },
      { text: 'Basic error handling with potential information disclosure', value: 2 },
      { text: 'Poor error handling that could expose sensitive information', value: 4 }
    ]
  },
  {
    id: 'ast07',
    title: 'AST07 - Insecure Storage',
    description: 'How does your skill store sensitive data?',
    options: [
      { text: 'No sensitive data stored or encrypted at rest', value: 0 },
      { text: 'Sensitive data encrypted and access controlled', value: 1 },
      { text: 'Some sensitive data stored but not properly secured', value: 2 },
      { text: 'Sensitive data stored in plain text or weakly protected', value: 4 }
    ]
  },
  {
    id: 'ast08',
    title: 'AST08 - Poor Scanning',
    description: 'How is your skill tested for security issues?',
    options: [
      { text: 'Regular security testing and automated scanning', value: 0 },
      { text: 'Some security testing but not comprehensive', value: 1 },
      { text: 'Basic testing, security not a primary focus', value: 2 },
      { text: 'No security testing or scanning performed', value: 4 }
    ]
  },
  {
    id: 'ast09',
    title: 'AST09 - Lack of Monitoring',
    description: 'How do you monitor your skill\'s behavior?',
    options: [
      { text: 'Comprehensive logging and monitoring in place', value: 0 },
      { text: 'Some monitoring but not complete coverage', value: 1 },
      { text: 'Basic monitoring or none at all', value: 2 },
      { text: 'No monitoring of skill behavior', value: 4 }
    ]
  },
  {
    id: 'ast10',
    title: 'AST10 - MAESTRO Misalignment',
    description: 'Does your skill align with security frameworks?',
    options: [
      { text: 'Follows security frameworks and best practices', value: 0 },
      { text: 'Some alignment but gaps exist', value: 1 },
      { text: 'Limited security consideration in design', value: 2 },
      { text: 'No consideration of security frameworks', value: 4 }
    ]
  }
];

let currentQuestion = 0;
let answers = {};

function initAssessment() {
  showQuestion(0);
  updateProgress();
}

function showQuestion(index) {
  const question = questions[index];
  document.getElementById('question-title').textContent = question.title;
  document.getElementById('question-description').textContent = question.description;

  const optionsContainer = document.getElementById('options-container');
  optionsContainer.innerHTML = '';

  question.options.forEach((option, optionIndex) => {
    const optionDiv = document.createElement('div');
    optionDiv.className = 'option-item';

    const radio = document.createElement('input');
    radio.type = 'radio';
    radio.name = 'option';
    radio.value = option.value;
    radio.id = `option-${optionIndex}`;

    if (answers[question.id] === option.value) {
      radio.checked = true;
    }

    const label = document.createElement('label');
    label.htmlFor = `option-${optionIndex}`;
    label.textContent = option.text;

    optionDiv.appendChild(radio);
    optionDiv.appendChild(label);
    optionsContainer.appendChild(optionDiv);
  });

  updateNavigation();
}

function updateProgress() {
  const progress = ((currentQuestion + 1) / questions.length) * 100;
  document.getElementById('progress-fill').style.width = `${progress}%`;
  document.getElementById('progress-text').textContent = `Question ${currentQuestion + 1} of ${questions.length}`;
}

function updateNavigation() {
  document.getElementById('prev-btn').disabled = currentQuestion === 0;
  document.getElementById('next-btn').textContent = currentQuestion === questions.length - 1 ? 'Finish' : 'Next';
}

function calculateResults() {
  let totalScore = 0;
  const maxScore = questions.length * 4;
  const riskBreakdown = [];

  questions.forEach(question => {
    const score = answers[question.id] || 0;
    totalScore += score;

    let riskLevel = 'Low';
    if (score >= 3) riskLevel = 'High';
    else if (score >= 2) riskLevel = 'Medium';

    riskBreakdown.push({
      id: question.id,
      title: question.title,
      score: score,
      riskLevel: riskLevel
    });
  });

  const riskPercentage = (totalScore / maxScore) * 100;

  return {
    totalScore,
    maxScore,
    riskPercentage,
    riskBreakdown
  };
}

function showResults() {
  const results = calculateResults();

  document.getElementById('assessment-container').style.display = 'none';
  document.getElementById('results-container').style.display = 'block';

  // Overall score
  document.getElementById('score-value').textContent = `${results.riskPercentage.toFixed(1)}%`;
  document.getElementById('score-fill').style.width = `${results.riskPercentage}%`;

  // Risk breakdown
  const riskItems = document.getElementById('risk-items');
  riskItems.innerHTML = '';

  results.riskBreakdown.forEach(item => {
    const itemDiv = document.createElement('div');
    itemDiv.className = `risk-item risk-${item.riskLevel.toLowerCase()}`;
    itemDiv.innerHTML = `
      <h4>${item.title}</h4>
      <p>Risk Level: ${item.riskLevel} (Score: ${item.score}/4)</p>
    `;
    riskItems.appendChild(itemDiv);
  });

  // Recommendations
  const mitigationList = document.getElementById('mitigation-list');
  mitigationList.innerHTML = '';

  if (results.riskPercentage < 25) {
    mitigationList.innerHTML = '<p>✅ Your skill appears to have good security practices. Continue monitoring and regular security reviews.</p>';
  } else if (results.riskPercentage < 50) {
    mitigationList.innerHTML = `
      <ul>
        <li>Review and minimize skill permissions</li>
        <li>Implement comprehensive input validation</li>
        <li>Add security testing to your development process</li>
        <li>Consider security code review</li>
      </ul>
    `;
  } else {
    mitigationList.innerHTML = `
      <ul>
        <li><strong>URGENT:</strong> Implement immediate security fixes</li>
        <li>Conduct thorough security audit</li>
        <li>Restrict skill permissions to minimum required</li>
        <li>Add encryption for sensitive data</li>
        <li>Implement proper error handling</li>
        <li>Add comprehensive logging and monitoring</li>
        <li>Consider professional security review</li>
      </ul>
    `;
  }
}

// Event listeners
document.getElementById('next-btn').addEventListener('click', () => {
  // Save current answer
  const selectedOption = document.querySelector('input[name="option"]:checked');
  if (selectedOption) {
    answers[questions[currentQuestion].id] = parseInt(selectedOption.value);
  }

  if (currentQuestion < questions.length - 1) {
    currentQuestion++;
    showQuestion(currentQuestion);
    updateProgress();
  } else {
    showResults();
  }
});

document.getElementById('prev-btn').addEventListener('click', () => {
  if (currentQuestion > 0) {
    currentQuestion--;
    showQuestion(currentQuestion);
    updateProgress();
  }
});

document.getElementById('retake-assessment').addEventListener('click', () => {
  currentQuestion = 0;
  answers = {};
  document.getElementById('results-container').style.display = 'none';
  document.getElementById('assessment-container').style.display = 'block';
  initAssessment();
});

document.getElementById('download-report').addEventListener('click', () => {
  const results = calculateResults();
  const report = {
    assessmentDate: new Date().toISOString(),
    overallRiskScore: results.riskPercentage,
    riskBreakdown: results.riskBreakdown,
    recommendations: document.getElementById('mitigation-list').innerText
  };

  const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'ast10-risk-assessment-report.json';
  a.click();
  URL.revokeObjectURL(url);
});

// Initialize assessment
initAssessment();
</script>

<style>
#assessment-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #f9f9f9;
}

#progress-bar {
  width: 100%;
  height: 30px;
  background: #eee;
  border-radius: 15px;
  margin-bottom: 20px;
  position: relative;
}

#progress-fill {
  height: 100%;
  background: #007acc;
  border-radius: 15px;
  transition: width 0.3s ease;
}

#progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #333;
  font-weight: bold;
}

#question-container {
  margin-bottom: 30px;
}

.option-item {
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background: white;
}

.option-item:hover {
  background: #f0f8ff;
}

.option-item input[type="radio"] {
  margin-right: 10px;
}

#navigation {
  display: flex;
  justify-content: space-between;
}

button {
  padding: 10px 20px;
  background: #007acc;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background: #005999;
}

#score-bar {
  width: 100%;
  height: 30px;
  background: #eee;
  border-radius: 15px;
  margin: 10px 0;
}

#score-fill {
  height: 100%;
  background: linear-gradient(to right, #4CAF50, #FFC107, #F44336);
  border-radius: 15px;
  transition: width 0.3s ease;
}

.risk-item {
  padding: 10px;
  margin: 5px 0;
  border-radius: 4px;
}

.risk-low { background: #e8f5e8; border-left: 4px solid #4CAF50; }
.risk-medium { background: #fff3e0; border-left: 4px solid #FFC107; }
.risk-high { background: #ffebee; border-left: 4px solid #F44336; }

#action-buttons {
  margin-top: 30px;
  display: flex;
  gap: 10px;
}
</style>

---

*This interactive tool helps assess AI agent skills against the OWASP AST10 framework. Results are for educational purposes and should be supplemented with professional security review.*</content>
<parameter name="filePath">c:\Users\kenhu\www-project-agentic-skills-top-10\risk-assessment.md