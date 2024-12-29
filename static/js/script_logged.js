function generateChoices(event) {
    event.preventDefault();

    const numberOfChoices = document.getElementById('Choice').value;
    const container = document.getElementById('choicesContainer');

    // Ajouter les champs pour chaque choix
    for (let i = 1; i <= numberOfChoices; i++) {
        const choiceInput = document.createElement('input');
        choiceInput.type = 'text';
        choiceInput.id = `choice${i}`;
        choiceInput.name = `choice${i}`;
        choiceInput.placeholder = `Entrez le choix ${i}`;
        choiceInput.required = true;

        container.appendChild(choiceInput); // Ajoute l'élément au conteneur
        container.appendChild(document.createElement('br')); // Ajoute un saut de ligne
    }

    console.log(`Number of choices: ${numberOfChoices}`);
}