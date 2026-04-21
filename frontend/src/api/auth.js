// src/api/auth.js
export const authApi = {
  async exchangeCodeForToken(code) {
    const response = await fetch("http://localhost:8000/auth/google/callback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
    });
    
    if (!response.ok) throw new Error("Failed to authenticate");
    return response.json();
  }
};