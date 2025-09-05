(() => {
    const editAcccountBtn = document.getElementById('editAccountBtn');
    editAcccountBtn.addEventListener('click', () => {
        window.location.href = editAcccountBtn.dataset.editAccountUrl;
    })
})();