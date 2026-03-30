import "./components.css";

type IncomingBubbleProps = {
  message: string;
};

export default function IncomingBubble({ message }: IncomingBubbleProps) {
  return (
    <div className="w-full flex justify-start">
      <div className="bubble incoming-bubble">{message}</div>
    </div>
  );
}
