/**
 * register.js — GreenField Local Hub (GLH)
 * Loaded on register.html and reset_password.html.
 *
 * Features:
 *   1. Live password strength meter
 *   2. Password-match indicator
 *   3. Client-side form validation feedback (non-blocking — server re-validates)
 */

(function () {
  "use strict";

  /* ─────────────────────────────────────────────
     STRENGTH METER
  ───────────────────────────────────────────── */

  const STRENGTH_CONFIG = [
    { label: "Too short",  color: "#b83232", width: "15%" },
    { label: "Weak",       color: "#d87030", width: "30%" },
    { label: "Fair",       color: "#c8780f", width: "55%" },
    { label: "Good",       color: "#2d7a27", width: "78%" },
    { label: "Strong",     color: "#1e5c1a", width: "100%" },
  ];

  /**
   * Score a password 0–4.
   * Criteria: length ≥8, has lowercase, uppercase, digit, special char.
   */
  function scorePassword(pw) {
    if (!pw || pw.length < 8) return 0;
    let score = 1;
    if (/[a-z]/.test(pw)) score++;
    if (/[A-Z]/.test(pw)) score++;
    if (/\d/.test(pw))    score++;
    if (/[^A-Za-z\d]/.test(pw)) score++;
    return Math.min(score - 1, 4); // 0..4
  }

  function updateStrengthUI(bar, label, pw) {
    if (!bar || !label) return;
    if (!pw) {
      bar.style.setProperty("--strength-width", "0%");
      bar.style.setProperty("--strength-color", "#e8e5de");
      label.textContent = "";
      label.style.color = "";
      return;
    }
    const s = scorePassword(pw);
    const cfg = STRENGTH_CONFIG[s];
    bar.style.setProperty("--strength-width", cfg.width);
    bar.style.setProperty("--strength-color", cfg.color);
    label.textContent  = cfg.label;
    label.style.color  = cfg.color;
  }

  /* ─────────────────────────────────────────────
     MATCH INDICATOR
  ───────────────────────────────────────────── */

  function updateMatchUI(matchEl, pw, confirm) {
    if (!matchEl) return;
    if (!confirm) { matchEl.textContent = ""; matchEl.className = "field-match"; return; }
    if (pw === confirm) {
      matchEl.textContent = "✓ Passwords match";
      matchEl.className   = "field-match match";
    } else {
      matchEl.textContent = "✗ Passwords don't match";
      matchEl.className   = "field-match no-match";
    }
  }

  /* ─────────────────────────────────────────────
     WIRE UP — REGISTER PAGE
  ───────────────────────────────────────────── */

  // Strength bar
  const pwInput       = document.getElementById("password");
  const strengthBar   = document.getElementById("strength-bar");
  const strengthLabel = document.getElementById("strength-label");

  if (pwInput && strengthBar) {
    pwInput.addEventListener("input", function () {
      updateStrengthUI(strengthBar, strengthLabel, pwInput.value);
    });
  }

  // Match indicator
  const confirmInput  = document.getElementById("confirm_password");
  const matchEl       = document.getElementById("password-match");

  if (confirmInput && matchEl) {
    function checkMatch() {
      updateMatchUI(matchEl, pwInput ? pwInput.value : "", confirmInput.value);
    }
    confirmInput.addEventListener("input", checkMatch);
    if (pwInput) pwInput.addEventListener("input", checkMatch);
  }

  /* ─────────────────────────────────────────────
     WIRE UP — ACCOUNT SETTINGS PAGE
  ───────────────────────────────────────────── */

  const settingsPwInput   = document.getElementById("new_password");
  const settingsBar       = document.getElementById("settings-strength-bar");
  const settingsLabel     = document.getElementById("settings-strength-label");
  const settingsConfirm   = document.getElementById("confirm_password"); // same id reused
  const settingsMatchEl   = document.getElementById("settings-password-match");

  if (settingsPwInput && settingsBar) {
    settingsPwInput.addEventListener("input", function () {
      updateStrengthUI(settingsBar, settingsLabel, settingsPwInput.value);
    });
  }

  if (settingsPwInput && settingsConfirm && settingsMatchEl) {
    function checkSettingsMatch() {
      updateMatchUI(settingsMatchEl, settingsPwInput.value, settingsConfirm.value);
    }
    settingsPwInput.addEventListener("input", checkSettingsMatch);
    settingsConfirm.addEventListener("input", checkSettingsMatch);
  }

  /* ─────────────────────────────────────────────
     WIRE UP — RESET PASSWORD PAGE
  ───────────────────────────────────────────── */

  const resetPwInput    = document.getElementById("new_password");
  const resetBar        = document.getElementById("reset-strength-bar");
  const resetLabel      = document.getElementById("reset-strength-label");
  const resetConfirm    = document.getElementById("confirm_password");
  const resetMatchEl    = document.getElementById("reset-password-match");

  if (resetPwInput && resetBar) {
    resetPwInput.addEventListener("input", function () {
      updateStrengthUI(resetBar, resetLabel, resetPwInput.value);
    });
  }

  if (resetPwInput && resetConfirm && resetMatchEl) {
    function checkResetMatch() {
      updateMatchUI(resetMatchEl, resetPwInput.value, resetConfirm.value);
    }
    resetPwInput.addEventListener("input", checkResetMatch);
    resetConfirm.addEventListener("input", checkResetMatch);
  }

})();