import { Navigate, useLocation } from "react-router-dom";
import type { ReactNode } from "react";
import { getCurrentUser } from "../api/client";

export default function RequireAuth({ children }: { children: ReactNode }) {
  const loc = useLocation();
  const user = getCurrentUser();

  if (!user) {
    return <Navigate to="/login" replace state={{ from: loc.pathname }} />;
  }

  if (loc.pathname.startsWith("/admin") && user.role && user.role !== "admin") {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
}
