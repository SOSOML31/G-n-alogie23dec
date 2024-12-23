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
                if (data.length === 0) {
                    treeContainer.innerHTML = "<p>Aucun individu dans l'arbre généalogique.</p>";
                } else {
                    treeContainer.innerHTML = "<pre>" + JSON.stringify(data, null, 2) + "</pre>";
                }
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
            const response = await fetch(`${apiUrl}/individus/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                alert("Individu ajouté avec succès !");
                loadArbre();
                event.target.reset();
            } else {
                const errorData = await response.json();
                alert(`Erreur : ${errorData.detail}`);
            }
        } catch (error) {
            console.error(error);
            alert("Une erreur est survenue lors de l'ajout de l'individu.");
        }
    });

    // Modifier un individu
    document.getElementById("modifier-form").addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(event.target);
        const data = Object.fromEntries(formData);
        const individuId = data.id; // Assurez-vous que le formulaire a un champ `id`
        delete data.id; // Retirez l'ID du corps de la requête

        try {
            const response = await fetch(`${apiUrl}/individus/${individuId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                alert("Individu modifié avec succès !");
                loadArbre();
                event.target.reset();
            } else {
                const errorData = await response.json();
                alert(`Erreur : ${errorData.detail}`);
            }
        } catch (error) {
            console.error(error);
            alert("Une erreur est survenue lors de la modification de l'individu.");
        }
    });

    // Supprimer un individu
    document.getElementById("supprimer-form").addEventListener("submit", async (event) => {
        event.preventDefault();

        const individuId = document.getElementById("delete_id").value;

        try {
            const response = await fetch(`${apiUrl}/individus/${individuId}`, {
                method: "DELETE",
            });

            if (response.ok) {
                alert("Individu supprimé avec succès !");
                loadArbre();
                event.target.reset();
            } else {
                const errorData = await response.json();
                alert(`Erreur : ${errorData.detail}`);
            }
        } catch (error) {
            console.error(error);
            alert("Une erreur est survenue lors de la suppression de l'individu.");
        }
    });

    // Charger l'arbre généalogique au démarrage
    loadArbre();
});