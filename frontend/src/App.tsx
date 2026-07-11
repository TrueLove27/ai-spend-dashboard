import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import DailyCosts from "./pages/DailyCosts";
import Agents from "./pages/Agents";
import Analytics from "./pages/Analytics";
import SyncLogs from "./pages/SyncLogs";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/daily" element={<DailyCosts />} />
        <Route path="/agents" element={<Agents />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/sync" element={<SyncLogs />} />
      </Routes>
    </Layout>
  );
}
