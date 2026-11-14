/* script.js - Simple UI interactions for Learnova */

document.addEventListener('DOMContentLoaded', function () {

  // Auto-dismiss alert messages after 4 seconds
  var alerts = document.querySelectorAll('.alert');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.opacity = '0';
      alert.style.transition = 'opacity 0.4s';
      setTimeout(function () { alert.remove(); }, 400);
    }, 4000);
  });

  // Auto-scroll message list to bottom
  var msgList = document.getElementById('msgList');
  if (msgList) {
    msgList.scrollTop = msgList.scrollHeight;
  }

  // Submit message form with Ctrl+Enter
  var msgArea = document.querySelector('.message-form-area textarea');
  if (msgArea) {
    msgArea.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        this.closest('form').submit();
      }
    });
  }

  // Preview avatar image before upload
  var avatarInput = document.querySelector('input[type="file"][name="avatar"]');
  if (avatarInput) {
    avatarInput.addEventListener('change', function () {
      var file = this.files[0];
      if (!file) return;
      var reader = new FileReader();
      reader.onload = function (e) {
        var preview = document.querySelector('.profile-avatar, .profile-avatar-initials');
        if (preview) {
          var img = document.createElement('img');
          img.src = e.target.result;
          img.className = 'profile-avatar';
          preview.replaceWith(img);
        }
      };
      reader.readAsDataURL(file);
    });
  }

});
