# React From Zero: Components, State, Props, and Hooks

This guide explains the foundational principles of **React** covered across Practicals 2 through 6 in `Assignment-4/react-practicals/`.

---

## 1. What is React, and Why Do We Use It?

In traditional web development (like Assignment 3), when data changes, you must manually find the HTML element using `document.getElementById(...)` and manually update its text:
```javascript
// Traditional Vanilla JS (Imperative approach):
const counter = document.getElementById("count");
let count = 0;
count++;
counter.textContent = count; // You have to manually update the DOM!
```

As an application grows to dozens of buttons, inputs, and tables, this manual DOM manipulation becomes messy, bug-prone, and difficult to maintain.

### The React Way (Declarative UI):
In **React**, you do not manipulate the DOM directly. Instead, you declare:
> *"Here is my data (State). Here is what the UI should look like for this data (JSX)."*

Whenever the data changes, **React automatically figures out what changed and updates the browser screen for you**.

---

## 2. What is a Component?

A **Component** is a self-contained, reusable building block of a user interface. 

Think of components like **Lego bricks**:
- One Lego brick might be a navigation bar (`<Navbar />`).
- Another brick might be a counter card (`<StateCounter />`).
- Another brick might be a student profile (`<StudentCard />`).

You assemble these smaller component bricks together inside `<App />` to construct an entire web application!

---

## 3. What is JSX?

Look at this line inside `FunctionStudent.jsx`:
```jsx
return (
  <div className="practical-card">
    <h2>Student Record</h2>
  </div>
);
```

This syntax looks like HTML, but it is written inside a JavaScript file! This is called **JSX (JavaScript XML)**.

### Key Rules of JSX:
1. **It compiles to real JavaScript**: Tools like Vite and Babel transform `<h2>Hello</h2>` into `React.createElement('h2', null, 'Hello')`.
2. **`className` instead of `class`**: Because `class` is a reserved keyword in JavaScript, we write `className="my-class"` in JSX.
3. **Curly Braces `{}` for JavaScript expressions**: Any valid JavaScript variable or expression can be injected directly into JSX using `{}`:
   ```jsx
   const studentName = "Jey";
   return <h3>Welcome, {studentName}!</h3>;
   ```

---

## 4. Function Components vs. Class Components

React offers two historical ways to create components:

### A. Modern Function Components (Practical 6)
A function component is simply a JavaScript function that returns JSX:
```jsx
// From FunctionStudent.jsx:
function FunctionStudent() {
  const name = "Jey";
  return <h3>Student: {name}</h3>;
}
export default FunctionStudent;
```
- **Why it's preferred today**: Shorter, easier to read, has no complicated `this` keyword, and can use React Hooks.

### B. Legacy Class Components (Practical 3)
A class component extends `React.Component` and must implement a `render()` method:
```jsx
// From ClassStudent.jsx:
class ClassStudent extends React.Component {
  constructor(props) {
    super(props);
    this.state = { name: "Jey" };
  }

  render() {
    return <h3>Student: {this.state.name}</h3>;
  }
}
export default ClassStudent;
```
- **Why it's taught in lab courses**: To help students understand the history of React and recognize class-based legacy code.

---

## 5. Props vs. State: The Fundamental Difference

Understanding the difference between **Props** and **State** is the #1 question asked in college lab evaluations:

| Feature | **Props** (Properties) | **State** |
| :--- | :--- | :--- |
| **Analogy** | Like **genes passed from parents to children**. | Like your **heart rate or mood** (internal and changing). |
| **Origin** | Passed **into** a component from its parent. | Created and managed **inside** the component itself. |
| **Mutability** | **Read-Only (Immutable)**. The child cannot change its props. | **Mutable** via its setter function (`setCount(...)`). |
| **Purpose** | Configures a component and shares data downward. | Stores interactive data that changes over time (inputs, toggles, counters). |
| **Demonstrated In** | Practical 4 (`StudentProps.jsx`) | Practical 2 (`StateCounter.jsx`) |

---

## 6. React State: `useState` (Practical 2)

Inside `StateCounter.jsx`:
```jsx
const [count, setCount] = useState(0);
```

### Breaking Down this Syntax (Array Destructuring):
1. `useState(0)`: Calls the React hook and initializes the state value to `0`.
2. `count`: The variable holding the current state value.
3. `setCount`: The **setter function** used to update the state.

```jsx
// When button is clicked:
<button onClick={() => setCount(count + 1)}>
  + Increment
</button>
```

> [!CAUTION]
> **Never modify state directly!** Never write `count = count + 1`. 
> React will not detect the change! You must always call the setter function: `setCount(count + 1)`. Calling `setCount` alerts React that a state change happened, prompting an immediate UI re-render.

---

## 7. React Props & List Rendering with `.map()` (Practical 4)

In `StudentProps.jsx`, the parent component has an array of student data:
```jsx
const studentsList = [
  { id: 1, name: "Jey", branch: "CSE" },
  { id: 2, name: "Aarav Sharma", branch: "ECE" }
];
```

The parent loops over the array using `.map()` and renders a child `<StudentCard />` for each item, passing data via attributes:
```jsx
{studentsList.map((student) => (
  <StudentCard
    key={student.id}
    name={student.name}
    branch={student.branch}
  />
))}
```

The child component receives those attributes as an argument:
```jsx
function StudentCard({ name, branch }) {
  return (
    <div className="card">
      <h3>{name}</h3>
      <p>{branch}</p>
    </div>
  );
}
```

> [!NOTE]
> The `key={student.id}` prop is required by React when rendering lists. It acts as an internal tracking ID so React knows which items were added, removed, or changed.

---

## 8. The Three Essential React Hooks (Practical 5)

Hooks are special functions starting with `use` that let function components "hook into" React features:

### 1. `useState` (Reactive State)
```jsx
const [clicks, setClicks] = useState(0);
```
Stores data that changes in response to user interaction and triggers a visual re-render.

### 2. `useRef` (DOM Node Reference without Re-rendering)
```jsx
const inputRef = useRef(null);

// Attach to element:
<input ref={inputRef} />

// Programmatically focus it when a button is clicked:
inputRef.current.focus();
```
`useRef` creates a direct pointer to a real browser DOM element. Unlike state, changing a ref's `.current` value does **not** trigger a re-render. It is perfect for focusing inputs, measuring elements, or storing timers.

### 3. `useEffect` (Side Effects & Lifecycle)
```jsx
useEffect(() => {
  document.title = `Clicked ${clicks} times — Hooks Demo`;

  return () => {
    // Cleanup function: runs when component unmounts
  };
}, [clicks]); // Dependency array: only runs when 'clicks' changes
```
A **side effect** is any operation that reaches outside React—such as fetching data from a server, setting a timer, or updating `document.title`. `useEffect` allows you to execute side effects cleanly after React has painted the screen.

Now let's examine the exact code implementation across all six practicals in [CODE-EXPLANATION.md](CODE-EXPLANATION.md)!
