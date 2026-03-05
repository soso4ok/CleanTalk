import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import PostListPage from "./pages/PostListPage";
import PostDetailPage from "./pages/PostDetailPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import { AuthProvider } from "./context/AuthContext";

export default function App() {
  return (
    <AuthProvider>
      <div className="flex min-h-screen flex-col bg-gray-50">
        <Navbar />
        <main className="mx-auto w-full max-w-4xl flex-1 px-4 py-8">
          <Routes>
            <Route path="/" element={<PostListPage />} />
            <Route path="/posts/:id" element={<PostDetailPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </AuthProvider>
  );
}
