import { NavLink } from "react-router-dom";
import { ReactNode } from "react";

const links = [
  { to: "/", label: "Overview" },
  { to: "/daily", label: "Daily Costs" },
  { to: "/workspaces", label: "Workspaces" },
  { to: "/analytics", label: "Analytics" },
  { to: "/sync", label: "Sync Logs" },
  { to: "/integrations", label: "Integrations" },
];

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="layout">
      <aside className="sidebar">
        <h1>Cloud Spend</h1>
        <p>SaaS Cost Control Tower</p>
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
