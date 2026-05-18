const SCORE_KEY = 'quiz_scores';

function getScores() {
  try {
    return JSON.parse(localStorage.getItem(SCORE_KEY) || '{}');
  } catch (error) {
    return {};
  }
}

function saveScore(levelPath, score, max) {
  const scores = getScores();
  const previous = scores[levelPath];
  if (!previous || score > previous.best) {
    scores[levelPath] = { best: score, max, date: new Date().toISOString() };
    localStorage.setItem(SCORE_KEY, JSON.stringify(scores));
  }
  return scores[levelPath] || previous;
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function setText(id, value) {
  const element = document.getElementById(id);
  if (element) element.textContent = value;
}

function show(element, visible) {
  if (element) element.classList.toggle('hidden', !visible);
}

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Request failed: ${response.status}`);
  return response.json();
}

function initLevelsPage() {
  const grid = document.getElementById('levels-grid');
  const empty = document.getElementById('empty-state');
  const count = document.getElementById('level-count');
  const scores = getScores();

  fetchJson('/api/levels')
    .then((levels) => {
      count.textContent = `${levels.length} level${levels.length === 1 ? '' : 's'}`;
      show(empty, levels.length === 0);

      grid.innerHTML = levels.map((level) => {
        const score = scores[level.path];
        const played = score ? `<span class="played-badge">Best ${score.best}/${score.max}</span>` : '';
        const thumb = level.thumbnail
          ? `<img class="level-thumb" src="${escapeHtml(level.thumbnail)}" alt="${escapeHtml(level.title)} thumbnail" loading="lazy">`
          : '';

        return `
          <a class="level-card" href="quiz.html?level=${encodeURIComponent(level.path)}">
            <div class="level-thumb-wrap">${thumb}${played}</div>
            <div class="level-body">
              <h2>${escapeHtml(level.title)}</h2>
              <p class="label">${escapeHtml(level.channel)}</p>
              <div class="level-meta">
                <span class="chip">${level.questionCount} otázek</span>
                <span class="score-chip">${level.maxPoints} bodů</span>
                ${level.date ? `<span class="chip">${escapeHtml(level.date)}</span>` : ''}
              </div>
            </div>
          </a>`;
      }).join('');
    })
    .catch((error) => {
      count.textContent = 'Offline';
      grid.innerHTML = `<section class="panel state-panel">Nepodařilo se načíst levely: ${escapeHtml(error.message)}</section>`;
    });
}

function sameSelection(selected, correct) {
  if (selected.length !== correct.length) return false;
  const selectedSet = new Set(selected);
  return correct.every((index) => selectedSet.has(index));
}

function initQuizPage() {
  const params = new URLSearchParams(window.location.search);
  const levelPath = params.get('level');
  const loading = document.getElementById('quiz-loading');
  const errorBox = document.getElementById('quiz-error');
  const quizScreen = document.getElementById('quiz-screen');
  const resultsScreen = document.getElementById('results-screen');
  const form = document.getElementById('answers-form');
  const feedback = document.getElementById('feedback');
  const submitButton = document.getElementById('submit-answer');
  const nextButton = document.getElementById('next-question');

  let level;
  let currentIndex = 0;
  let score = 0;
  let answered = false;
  const results = [];

  function fail(message) {
    show(loading, false);
    show(errorBox, true);
    errorBox.textContent = message;
    setText('quiz-status', 'Error');
  }

  if (!levelPath) {
    fail('Chybí parametr level. Vrať se na výběr levelů.');
    return;
  }

  function maxPoints() {
    return level.questions.reduce((total, question) => total + Number(question.points || 0), 0);
  }

  function renderQuestion() {
    const question = level.questions[currentIndex];
    answered = false;
    show(feedback, false);
    show(submitButton, true);
    show(nextButton, false);

    const progress = ((currentIndex + 1) / level.questions.length) * 100;
    document.getElementById('progress-bar').style.width = `${progress}%`;
    setText('quiz-status', `${score}/${maxPoints()} pts`);
    setText('question-counter', `Otázka ${currentIndex + 1} z ${level.questions.length}`);
    setText('question-type', question.type === 'multi' ? 'multi-select' : 'single-select');
    setText('question-points', `${Number(question.points || 0)} pts`);
    setText('question-text', question.question || 'Bez textu otázky');

    const inputType = question.type === 'multi' ? 'checkbox' : 'radio';
    form.innerHTML = (question.options || []).map((option, index) => `
      <label class="answer-option" data-index="${index}">
        <input type="${inputType}" name="answer" value="${index}">
        <span>${escapeHtml(option)}</span>
      </label>
    `).join('');
  }

  function selectedAnswers() {
    return Array.from(form.querySelectorAll('input:checked')).map((input) => Number(input.value));
  }

  function submitAnswer() {
    if (answered) return;
    const question = level.questions[currentIndex];
    const selected = selectedAnswers();
    if (selected.length === 0) {
      feedback.textContent = 'Vyber alespoň jednu odpověď.';
      feedback.className = 'feedback fail';
      show(feedback, true);
      return;
    }

    answered = true;
    const correct = Array.isArray(question.correct) ? question.correct : [];
    const isCorrect = sameSelection(selected, correct);
    const points = isCorrect ? Number(question.points || 0) : 0;
    score += points;
    results.push({ question: question.question, earned: points, max: Number(question.points || 0), correct: isCorrect });

    form.querySelectorAll('.answer-option').forEach((option) => {
      const index = Number(option.dataset.index);
      const input = option.querySelector('input');
      input.disabled = true;
      if (correct.includes(index)) option.classList.add('correct');
      if (selected.includes(index) && !correct.includes(index)) option.classList.add('incorrect');
    });

    const correctText = correct.map((index) => question.options[index]).filter(Boolean).join(', ');
    feedback.textContent = isCorrect
      ? `Správně. +${points} bodů.`
      : `Špatně. Správná odpověď: ${correctText || 'není uvedena'}.`;
    feedback.className = `feedback ${isCorrect ? 'success' : 'fail'}`;
    show(feedback, true);
    show(submitButton, false);
    show(nextButton, true);
  }

  function renderResults() {
    const max = maxPoints();
    const saved = saveScore(levelPath, score, max);
    show(quizScreen, false);
    show(resultsScreen, true);
    setText('quiz-status', 'Complete');
    setText('final-score', `${score} / ${max}`);
    setText('best-score', `Nejlepší skóre: ${saved.best} / ${saved.max}`);
    document.getElementById('results-list').innerHTML = results.map((result, index) => `
      <div class="result-row">
        <strong>${index + 1}. ${escapeHtml(result.question || 'Otázka')}</strong>
        <span class="${result.correct ? 'score-chip' : 'chip'}">${result.earned}/${result.max}</span>
      </div>
    `).join('');
  }

  function nextQuestion() {
    if (currentIndex + 1 >= level.questions.length) {
      renderResults();
      return;
    }
    currentIndex += 1;
    renderQuestion();
  }

  submitButton.addEventListener('click', submitAnswer);
  nextButton.addEventListener('click', nextQuestion);

  fetchJson(`/api/level?path=${encodeURIComponent(levelPath)}`)
    .then((data) => {
      level = data;
      if (!Array.isArray(level.questions) || level.questions.length === 0) {
        fail('Level neobsahuje žádné otázky.');
        return;
      }

      document.getElementById('quiz-thumb').src = level.thumbnail || '';
      document.getElementById('quiz-thumb').alt = `${level.title || 'Video'} thumbnail`;
      setText('quiz-title', level.title || 'Untitled Level');
      setText('quiz-channel', `${level.channel || 'Unknown Channel'}${level.date ? ` · ${level.date}` : ''}`);
      show(loading, false);
      show(quizScreen, true);
      renderQuestion();
    })
    .catch((error) => fail(`Nepodařilo se načíst level: ${error.message}`));
}

if (document.body.dataset.page === 'levels') {
  initLevelsPage();
} else if (document.body.dataset.page === 'quiz') {
  initQuizPage();
}
