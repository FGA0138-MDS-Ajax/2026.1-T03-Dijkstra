// Os scripts JavaScript front-end do projeto. 
// Ele controla a lógica da tela


/*** Efeitos Visuais e Lógica Interativa para o Sistema NextBook*/

function setupBookForm() {
    const bookTypeSelect = document.querySelector('#book_type'); 
    const copiesContainer = document.querySelector('#copies-container');

    if (!bookTypeSelect || !copiesContainer) {
        return; 
    }
    const toggleCopiesInput = () => {
        if (bookTypeSelect.value === 'Digital') {
            copiesContainer.style.display = 'none';
        } else {
            copiesContainer.style.display = 'block';
        }
    };
    toggleCopiesInput();
    bookTypeSelect.addEventListener('change', toggleCopiesInput);
}

function setupDescriptionModals() {
    const modalTriggers = document.querySelectorAll('.modal-trigger');
    const closeButtons = document.querySelectorAll('.modal-close-btn');

    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            const modalId = trigger.getAttribute('data-modal-id');
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.style.display = 'block';
            }
        });
    });

    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const modalId = button.getAttribute('data-modal-id');
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.style.display = 'none';
            }
        });
    });

    window.addEventListener('click', (event) => {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    console.log("NextBook JS: Página carregada. Iniciando scripts...");
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease-in-out';
        document.body.style.opacity = '1';
    }, 100);        
    const userMenuButton = document.querySelector('.user-menu-button');
    if (userMenuButton) {
        const dropdown = userMenuButton.nextElementSibling;
        userMenuButton.addEventListener('click', function(event) {
            event.stopPropagation();
            dropdown.classList.toggle('show');
        });
        window.addEventListener('click', function(event) {
            if (userMenuButton && !userMenuButton.contains(event.target) && dropdown.classList.contains('show')) {
                dropdown.classList.remove('show');
            }
        });
    }
    const toggleBtn = document.getElementById('toggle-transfer-btn');
    const content = document.getElementById('transfer-content');

    if (toggleBtn && content) {
        console.log("NextBook JS: Botão e conteúdo de transferência encontrados.");
        toggleBtn.addEventListener('click', function() {
            console.log("NextBook JS: Botão de transferência clicado!");
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
            } else {
                content.style.maxHeight = (content.scrollHeight + 20) + "px";
            }
        });
    } else {
        console.log("NextBook JS: Botão ou conteúdo de transferência NÃO encontrados nesta página.");
    }    
    setupBookForm();

    setupDescriptionModals();
});