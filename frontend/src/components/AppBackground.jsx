import { FloatingLines } from "react-bits";

export default function AppBackground({ children }) {
    return (
        <FloatingLines
            lineColor="rgba(139, 92, 246, 0.6)"   // violet
            backgroundColor="#020617"            // deep dark blue
            lineWidth={1}
            lineCount={25}
            speed={0.4}
        >
            {children}
        </FloatingLines>
    );
}
