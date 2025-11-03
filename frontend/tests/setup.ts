import "@testing-library/jest-dom";
import "whatwg-fetch";
import { act } from "@testing-library/react";
import { useAuth } from "../lib/store";

afterEach(() => {
  act(() => {
    useAuth.setState({ user: null, initialized: false });
  });
});
