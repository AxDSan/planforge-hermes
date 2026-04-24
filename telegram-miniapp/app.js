/**
 * PlanForge Mini App — Main Logic
 * 
 * Initializes Telegram WebApp, fetches project status,
 * renders phases, handles user interactions.
 */

// Initialize Telegram WebApp
const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

// Theme handling
document.body.style.backgroundColor = tg.backgroundColor;
document.body.style.color = tg.textColor;

// Main app logic
const App = {
  data: null,

  async init() {
    this.bindEvents();
    await this.loadStatus();
  },

  bindEvents() {
    document.getElementById('btn-refresh').addEventListener('click', () => {
      tg.showProgress();
      this.loadStatus().then(() => {
        tg.hideProgress();
      });
    });

    document.getElementById('btn-status').addEventListener('click', () => {
      // Send data back to bot (Hermes can read this)
      API.sendCommand('/planforge-status');
      tg.showAlert('Status command sent to Hermes!');
    });
  },

  async loadStatus() {
    this.data = await API.getStatus();
    this.render();
  },

  render() {
    if (!this.data) return;

    // Project name
    document.getElementById('project-name').textContent = this.data.project;

    // Overall progress
    const totalProgress = this.data.phases.reduce((a, p) => a + p.progress, 0) / this.data.phases.length;
    document.getElementById('progress-text').textContent = Math.round(totalProgress) + '%';
    document.getElementById('progress-fill').style.width = totalProgress + '%';

    // Phases
    const phasesList = document.getElementById('phases-list');
    phasesList.innerHTML = '';

    this.data.phases.forEach(phase => {
      const card = document.createElement('div');
      card.className = `phase-card ${phase.number === this.data.currentPhase ? 'active' : ''}`;

      const iconClass = phase.status === 'completed' ? 'done' :
                       phase.status === 'in_progress' ? 'active' :
                       phase.status === 'blocked' ? 'blocked' : 'pending';
      const icon = phase.status === 'completed' ? '✓' :
                  phase.status === 'in_progress' ? '●' :
                  phase.status === 'blocked' ? '!' : '○';

      card.innerHTML = `
        <div class="phase-icon ${iconClass}">${icon}</div>
        <div class="phase-info">
          <div class="phase-name">Phase ${phase.number}: ${phase.name}</div>
          <div class="phase-status">${this._formatStatus(phase.status)}</div>
        </div>
        <div class="phase-progress">${phase.progress}%</div>
      `;

      phasesList.appendChild(card);
    });

    // Set header color based on status
    if (this.data.locked) {
      tg.setHeaderColor('#ff9500'); // Orange when locked
    } else {
      tg.setHeaderColor('#34c759'); // Green when free
    }
  },

  _formatStatus(status) {
    const map = {
      'completed': '✅ Complete',
      'in_progress': '🔄 In Progress',
      'pending': '⏳ Pending',
      'blocked': '⚠️ Blocked'
    };
    return map[status] || status;
  }
};

// Start
App.init();
