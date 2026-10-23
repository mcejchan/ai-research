function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function filterLevels(levels, difficulty) {
  return difficulty === 'all' ? levels : levels.filter((level) => level.difficulty === difficulty);
}

function renderLevelCards(levels, scores = {}) {
  return levels.map((level) => {
    const score = scores[level.path];
    const played = score ? `<span class="played-badge">Best ${score.best}/${score.max}</span>` : '';
    const thumb = level.thumbnail
      ? `<img class="level-thumb" src="${escapeHtml(level.thumbnail)}" alt="${escapeHtml(level.title)} thumbnail" loading="lazy">`
      : '';
    const difficulty = level.difficulty || null;
    const label = difficulty === 'extra-easy' ? 'Extra Easy' : difficulty === 'easy' ? 'Easy' : difficulty === 'hard' ? 'Hard' : null;
    return `<a class="level-card" href="quiz.html?level=${encodeURIComponent(level.path)}"><div class="level-thumb-wrap">${thumb}${played}${label ? `<span class="difficulty-badge difficulty-${difficulty}">${label}</span>` : ''}</div><div class="level-body"><h2>${escapeHtml(level.title)}</h2><p class="label">${escapeHtml(level.channel)}</p><div class="level-meta"><span class="chip">${level.questionCount} otázek</span><span class="score-chip">${level.maxPoints} bodů</span>${level.date ? `<span class="chip">${escapeHtml(level.date)}</span>` : ''}</div></div></a>`;
  }).join('');
}

function evaluateAnswer(selected, question) {
  if (!selected.length) return { message: 'Vyber alespoň jednu odpověď.' };
  const correctIndexes = Array.isArray(question.correct) ? question.correct : [];
  const selectedSet = new Set(selected);
  const correct = selected.length === correctIndexes.length && correctIndexes.every((index) => selectedSet.has(index));
  const earned = correct ? Number(question.points || 0) : 0;
  const correctText = correctIndexes.map((index) => question.options[index]).filter(Boolean).join(', ');
  return {
    correct, earned, max: Number(question.points || 0), correctIndexes,
    feedback: correct ? `Správně. +${earned} bodů.` : `Špatně. Správná odpověď: ${correctText || 'není uvedena'}.`,
    explanation: question.explanation,
  };
}

function createQuizSession({ levelPath, questions, saveScore }) {
  let index = 0;
  let score = 0;
  let answered = false;
  const results = [];
  const max = questions.reduce((total, question) => total + Number(question.points || 0), 0);
  return {
    current: () => questions[index],
    progress: () => ({ index, total: questions.length, score, max, status: `${score}/${max} pts` }),
    submit(selected) {
      if (answered) return { message: 'answered' };
      const question = questions[index];
      const answer = evaluateAnswer(selected, question);
      if (answer.message) return answer;
      answered = true;
      score += answer.earned;
      results.push({ question: question.question, earned: answer.earned, max: answer.max, correct: answer.correct });
      return answer;
    },
    next() {
      if (index + 1 < questions.length) { index += 1; answered = false; return { complete: false, question: questions[index] }; }
      return { complete: true, score, max, best: saveScore(levelPath, score, max), results };
    },
  };
}

const quizPageLogic = { escapeHtml, filterLevels, renderLevelCards, evaluateAnswer, createQuizSession };
if (typeof module !== 'undefined') module.exports = quizPageLogic;
if (typeof globalThis !== 'undefined') globalThis.quizPageLogic = quizPageLogic;
