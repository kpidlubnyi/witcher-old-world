export const authApi = {
  async exchangeCodeForToken(code) {
    const response = await fetch("http://localhost:8000/auth/google/callback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
      credentials: "include", 
    });
    
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Failed to authenticate");
    }
    return response.json();
  }
};