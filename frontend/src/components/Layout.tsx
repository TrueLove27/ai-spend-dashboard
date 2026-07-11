import { NavLink, Outlet } from "react-router-dom";

const navItems = [
  { to: "/", label: "Overview", end: true },
  { to: "/daily", label: "Daily Costs" },
  { to: "/agents", label: "Agents" },
  { to: "/analytics", label: "Analytics" },
  { to: "/sync", label: "Sync Pipeline" },
];

export default function Layout() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">SC</div>
          <div>
            <h1>Spend Control</h1>
            <p>AI Voice &amp; LLM Costs</p>
          </div>
        </div>
        <nav>
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <footer className="sidebar-footer">
          <span className="status-dot" />
          Live demo · synthetic billing data
        </footer>
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
