import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import DailyCosts from "./pages/DailyCosts";
import Workspaces from "./pages/Workspaces";
import Analytics from "./pages/Analytics";
import SyncLogs from "./pages/SyncLogs";
import Integrations from "./pages/Integrations";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/daily" element={<DailyCosts />} />
        <Route path="/workspaces" element={<Workspaces />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/sync" element={<SyncLogs />} />
        <Route path="/integrations" element={<Integrations />} />
      </Routes>
    </Layout>
  );
}
