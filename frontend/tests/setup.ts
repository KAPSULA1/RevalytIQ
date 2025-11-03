import "@testing-library/jest-dom";
import "whatwg-fetch";
import { useAuth } from "../lib/store";

afterEach(() => {
  useAuth.setState({ user: null, initialized: false });
});
