document.addEventListener("DOMContentLoaded", () => {
    const apiUrl = "http://127.0.0.1:8000";

    // Charger l'arbre généalogique
    const loadArbre = async () => {
        const treeContainer = document.getElementById("arbre-genealogique");
        treeContainer.innerHTML = "<p>Chargement de l'arbre généalogique...</p>";

        try {
            const response = await fetch(`${apiUrl}/arbre`);
            const data = await response.json();

            if (response.ok) {
                treeContainer.innerHTML = JSON.stringify(data, null, 2);
            } else {
                treeContainer.innerHTML = "<p>Erreur lors du chargement de l'arbre généalogique.</p>";
            }
        } catch (error) {
            console.error(error);
            treeContainer.innerHTML = "<p>Impossible de charger l'arbre généalogique.</p>";
        }
    };

    // Ajouter un individu
    document.getElementById("ajout-form").addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(event.target);
        const data = Object.fromEntries(formData);

        try {
            const response = await fetch(`${apiUrl}/ajouter`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                alert("Individu ajouté avec succès !");
                loadArbre();
            } else {
                alert("Erreur lors de l'ajout de l'individu.");
            }
        } catch (error) {
            console.error(error);
        }
    });

    // Modifier un individu
    document.getElementById("modifier-form").addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(event.target);
        const data = Object.fromEntries(formData);

        try {
            const response = await fetch(`${apiUrl}/modifier/${data.individu_id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                alert("Individu modifié avec succès !");
                loadArbre();
            } else {
                alert("Erreur lors de la modification.");
            }
        } catch (error) {
            console.error(error);
        }
    });

    // Supprimer un individu
    document.getElementById("supprimer-form").addEventListener("submit", async (event) => {
        event.preventDefault();

        const individuId = document.getElementById("delete_id").value;

        try {
            const response = await fetch(`${apiUrl}/supprimer/${individuId}`, {
                method: "DELETE",
            });

            if (response.ok) {
                alert("Individu supprimé avec succès !");
                loadArbre();
            } else {
                alert("Erreur lors de la suppression.");
            }
        } catch (error) {
            console.error(error);
        }
    });

    // Charger l'arbre généalogique au démarrage
    loadArbre();
});