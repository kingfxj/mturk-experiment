import React from "react";

// NotFoundPage for unassigned paths + redirecting back to Home Page
export const NotFoundPage = () => {
  return (
    <div style={{ color: "black" }}>
      <p>The page you are looking for is temporarily unavailable.</p>
      <p>
        Please return to the <a href="./">Home Page</a>.
      </p>
    </div>
  );
};
