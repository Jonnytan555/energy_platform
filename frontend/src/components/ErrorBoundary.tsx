import React from "react";

export class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { error?: Error }
> {
  state: { error?: Error } = {};

  static getDerivedStateFromError(error: Error) {
    return { error };
  }

  render() {
    if (this.state.error) {
      return (
        <div style={{ padding: 16 }}>
          <h2>React crashed</h2>
          <pre>{String(this.state.error.message)}</pre>
        </div>
      );
    }
    return this.props.children;
  }
}
