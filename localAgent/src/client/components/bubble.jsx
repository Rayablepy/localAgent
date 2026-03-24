import './components.css';

export default function Bubble() {
  return (
      <div className="flex items-start gap-2.5">
        <div
            className="flex flex-col w-full max-w-[320px] leading-1.5 p-4 bg-neutral-secondary-soft rounded-e-base rounded-es-base">
          <div className="flex items-center space-x-1.5 rtl:space-x-reverse">
            <span className="text-amber-50 text-sm font-semibold text-heading">User</span>
          </div>
          <p className="text-amber-50 text-sm py-2.5 text-body">Some text</p>
        </div>
      </div>
  )
}