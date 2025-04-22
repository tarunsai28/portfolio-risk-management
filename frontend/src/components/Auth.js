import React, { useState } from 'react';
import { loginUser, registerUser } from "../services/api";  

const Auth = () => {
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const [isLogin, setIsLogin] = useState(true);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage(""); // Clear previous messages

        try {
            console.log("🔹 Sending Request...");
            const userData = { email, password, ...(isLogin ? {} : { username }) };
            console.log("📤 Request Data:", userData);

            const response = isLogin ? await loginUser(userData) : await registerUser(userData);
            console.log("✅ API Response:", response);

            if (isLogin) {
                setMessage(`🟢 Login successful! Token: ${response.data.token}`);
                localStorage.setItem("token", response.data.token); // Save token for future requests
            } else {
                setMessage("🟢 Registration successful! Please log in.");
            }
        } catch (error) {
            console.error("❌ Error:", error);

            // More detailed error handling
            if (error.response) {
                console.log("🔴 Server Error Response:", error.response.data);
                setMessage(error.response.data.error || "Something went wrong");
            } else if (error.request) {
                console.log("🔴 No Response Received:", error.request);
                setMessage("Server is not responding. Check if Flask is running.");
            } else {
                console.log("🔴 Other Error:", error.message);
                setMessage("An unexpected error occurred.");
            }
        }
    };

    return (
        <div>
            <h2>{isLogin ? "Login" : "Register"}</h2>
            <form onSubmit={handleSubmit}>
                {!isLogin && (
                    <input
                        type="text"
                        placeholder="Username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                )}
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">{isLogin ? "Login" : "Register"}</button>
            </form>
            <button onClick={() => setIsLogin(!isLogin)}>
                {isLogin ? "Switch to Register" : "Switch to Login"}
            </button>
            {message && <p>{message}</p>}
        </div>
    );
};

export default Auth;
