document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.descriptions-container').forEach(function(container) {
        var hidden = container.querySelector('input[type="hidden"]');
        var addBtn = container.querySelector('.add-desc');

        function updateHidden() {
            var textareas = container.querySelectorAll('.description-textarea');
            var values = Array.from(textareas).map(function(t) { return t.value; });
            hidden.value = JSON.stringify(values);
        }

        addBtn.addEventListener('click', function() {
            var textarea = document.createElement('textarea');
            textarea.rows = 3;
            textarea.cols = 50;
            textarea.className = 'description-textarea';
            var removeBtn = document.createElement('button');
            removeBtn.type = 'button';
            removeBtn.className = 'remove-desc';
            removeBtn.textContent = 'Remove';
            removeBtn.addEventListener('click', function() {
                container.removeChild(textarea);
                container.removeChild(removeBtn);
                var br = removeBtn.nextElementSibling;
                if (br && br.tagName === 'BR') container.removeChild(br);
                updateHidden();
            });
            var br = document.createElement('br');
            container.insertBefore(textarea, addBtn);
            container.insertBefore(removeBtn, addBtn);
            container.insertBefore(br, addBtn);
            updateHidden();
        });

        container.addEventListener('input', function(e) {
            if (e.target.classList.contains('description-textarea')) {
                updateHidden();
            }
        });

        // For existing remove buttons
        container.querySelectorAll('.remove-desc').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var textarea = btn.previousElementSibling;
                var br = btn.nextElementSibling;
                container.removeChild(textarea);
                container.removeChild(btn);
                if (br && br.tagName === 'BR') container.removeChild(br);
                updateHidden();
            });
        });
    });
});
