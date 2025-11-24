async function uploadAudio() {
    const file = document.getElementById('audioFile').files[0];
    if (!file) {
      alert("Choisissez un fichier audio !");
      return;
    }
  
    const formData = new FormData();
    formData.append("audio", file);
  
    try {
      const response = await fetch("http://127.0.0.1:5000/transcribe", {  // ✅ bon port
        method: "POST",
        body: formData
      });
  
      if (!response.ok) throw new Error("Erreur serveur : " + response.status);
      const data = await response.json();
      document.getElementById("result").textContent = data.text || "Aucun texte détecté.";
    } catch (error) {
      console.error("Erreur :", error);
      alert("Erreur de connexion avec le serveur Flask !");
    }
  }
  