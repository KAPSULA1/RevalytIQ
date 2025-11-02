"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { isAxiosError } from "axios";
import { register } from "@/lib/auth";

export default function SignupPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [feedback, setFeedback] = useState("");

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!username.trim() || !email.trim() || !password.trim() || !password2.trim()) {
      setError("All fields are required.");
      setFeedback("");
      return;
    }
    if (password !== password2) {
      setError("Passwords do not match.");
      setFeedback("");
      return;
    }

    setError("");
    setFeedback("");
    setIsSubmitting(true);

    try {
      await register(username.trim(), email.trim(), password, password2);
      setFeedback("Account created! Please sign in.");
      router.push("/");
    } catch (err: unknown) {
      let message = "Unable to sign up. Please try again.";
      if (isAxiosError(err)) {
        if (typeof err.response?.data === "string") {
          message = err.response.data;
        } else if (err.response?.data && typeof err.response.data === "object") {
          const data = err.response.data as Record<string, unknown>;
          const errors = (data.errors ?? data) as Record<string, unknown>;
          const messages = Object.values(errors)
            .map((value) => (Array.isArray(value) ? value.join(" ") : typeof value === "string" ? value : ""))
            .filter(Boolean);
          if (messages.length) message = messages.join(" ");
        }
      }
      setError(message);
      setFeedback("");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <form onSubmit={handleSubmit} data-testid="signup-form"
        className="bg-white shadow-lg rounded-2xl p-6 w-96 flex flex-col gap-4">
        <h2 className="text-2xl font-semibold text-center">Create Account</h2>

        <input type="text" placeholder="Username" value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="border p-2 rounded-lg focus:ring focus:ring-blue-300" />

        <input type="email" placeholder="Email" value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border p-2 rounded-lg focus:ring focus:ring-blue-300" />

        <input type="password" placeholder="Password" value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border p-2 rounded-lg focus:ring focus:ring-blue-300" />

        <input type="password" placeholder="Confirm password" value={password2}
          onChange={(e) => setPassword2(e.target.value)}
          className="border p-2 rounded-lg focus:ring focus:ring-blue-300" />

        {error && <p className="text-red-600 text-sm text-center">{error}</p>}
        {feedback && <p className="text-sm text-center text-blue-600" role="status">{feedback}</p>}

        <button type="submit" disabled={isSubmitting}
          className="bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-70">
          {isSubmitting ? "Signing Up..." : "Sign Up"}
        </button>
      </form>
    </div>
  );
}
