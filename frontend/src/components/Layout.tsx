import { NavLink } from "react-router-dom";
import { ReactNode } from "react";

const links = [
  { to: "/", label: "Overview" },
  { to: "/daily", label: "Daily Costs" },
  { to: "/agents", label: "Agents" },
  { to: "/analytics", label: "Analytics" },
  { to: "/sync", label: "Sync Logs" },
];

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="layout">
      <aside className="sidebar">
        <h1>AI Spend</h1>
        <p>Voice &amp; LLM Cost Control</p>
        <nav className="nav">
          {links.map((l) => (
            <NavLink key={l.to} to={l.to} end={l.to === "/"}>
              {l.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="main">{children}</main>
    </div>
  );
}
