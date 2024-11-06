// static/js/custom_subject.js
document.addEventListener('DOMContentLoaded', function() {
    const subjectSelect = document.getElementById('subject-select');
    const customSubjectInput = document.getElementById('custom-subject');

    subjectSelect.addEventListener('change', function() {
        if (this.value === '自定义') {
            customSubjectInput.style.display = 'block'; // 显示自定义输入框
            customSubjectInput.value = ''; // 清空自定义主题输入框
        } else {
            customSubjectInput.style.display = 'none'; // 隐藏自定义输入框
            customSubjectInput.value = this.value; // 将选定的主题填入
        }
    });
});
