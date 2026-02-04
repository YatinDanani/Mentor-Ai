# Dark Theme Customization Guide

This guide explains how to customize and extend the dark professional theme used in MentorAI.

## Color Palette

The theme uses a carefully selected dark color palette optimized for readability and visual appeal.

### Base Colors

| Token | Value | Usage |
|-------|-------|-------|
| `background` | `#0f0f0f` | Main page background |
| `surface` | `#1a1a1a` | Card/panel backgrounds |
| `surface-hover` | `#252525` | Hover states for surfaces |
| `border` | `#333333` | Borders and dividers |

### Text Colors

| Token | Value | Usage |
|-------|-------|-------|
| `text-primary` | `#ffffff` | Headings and important text |
| `text-secondary` | `#a1a1aa` | Body text and descriptions |
| `text-muted` | `#71717a` | Secondary info and placeholders |

### Brand Colors

| Token | Value | Usage |
|-------|-------|-------|
| `primary` | `#6366f1` | Primary actions, links, user messages |
| `primary-hover` | `#4f46e5` | Hover states for primary elements |
| `secondary` | `#8b5cf6` | Accents, highlights |

### Status Colors

| Token | Value | Usage |
|-------|-------|-------|
| `success` | `#22c55e` | Success messages, confirmations |
| `warning` | `#f59e0b` | Warnings, alerts |
| `error` | `#ef4444` | Errors, danger actions |
| `info` | `#3b82f6` | Informational messages |

## Typography

### Font Families

```typescript
// tailwind.config.ts
{
  fontFamily: {
    sans: ['Inter', 'sans-serif'],
    mono: ['JetBrains Mono', 'monospace'],
  },
}
```

### Custom Fonts

To use custom fonts:

1. Add Google Fonts import in `app/layout.tsx`:
```typescript
import { YourFont } from 'next/font/google'

const yourFont = YourFont({
  subsets: ['latin'],
  variable: '--font-your-font',
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={yourFont.variable}>
      <body>{children}</body>
    </html>
  )
}
```

2. Update `tailwind.config.ts`:
```typescript
{
  fontFamily: {
    sans: ['var(--font-your-font)', 'sans-serif'],
    mono: ['JetBrains Mono', 'monospace'],
  },
}
```

## Component Styling Guidelines

### Buttons

```tsx
// Primary Button
<button className="bg-primary hover:bg-primary-hover text-white px-4 py-2 rounded-md transition-colors duration-150">
  Action
</button>

// Secondary Button
<button className="bg-surface hover:bg-surface-hover border border-border text-text-primary px-4 py-2 rounded-md transition-colors duration-150">
  Cancel
</button>
```

### Inputs

```tsx
<input
  type="text"
  className="bg-surface border border-border text-text-primary placeholder-text-muted rounded-md px-3 py-2 focus:outline-none focus:border-primary transition-colors duration-150"
  placeholder="Enter text..."
/>
```

### Cards

```tsx
<div className="bg-surface border border-border rounded-md p-4">
  <h2 className="text-text-primary text-lg font-semibold mb-2">Card Title</h2>
  <p className="text-text-secondary">Card content goes here</p>
</div>
```

### Messages

```tsx
// User message
<div className="bg-primary text-white rounded-tl-md rounded-tr-md rounded-bl-md px-4 py-2">
  User message
</div>

// AI message
<div className="bg-surface border border-border text-text-primary rounded-tl-md rounded-tr-md rounded-br-md px-4 py-2">
  AI response
</div>
```

### Modals

```tsx
<div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center">
  <div className="bg-surface border border-border rounded-lg max-w-md w-full mx-4">
    <div className="p-4">
      <h3 className="text-text-primary text-lg font-semibold mb-2">Modal Title</h3>
      <p className="text-text-secondary">Modal content</p>
    </div>
    <div className="border-t border-border p-4 flex justify-end gap-2">
      <button className="px-4 py-2 text-text-primary hover:bg-surface-hover rounded-md">Cancel</button>
      <button className="px-4 py-2 bg-primary hover:bg-primary-hover text-white rounded-md">Confirm</button>
    </div>
  </div>
</div>
```

## Customizing Colors

### Change Accent Color

To change the primary accent color (e.g., from indigo to blue):

```typescript
// tailwind.config.ts
colors: {
  // ... other colors
  primary: '#3b82f6',        // Blue instead of indigo
  'primary-hover': '#2563eb',
}
```

### Add New Color

To add a custom accent color:

```typescript
// tailwind.config.ts
colors: {
  // ... existing colors
  accent: '#00d4ff',
  'accent-hover': '#00b8e6',
}
```

Usage:
```tsx
<button className="bg-accent hover:bg-accent-hover text-white">
  Custom Button
</button>
```

## Customizing Fonts

### Replace Primary Font

```typescript
// tailwind.config.ts
{
  fontFamily: {
    sans: ['YourFont', 'sans-serif'],
    mono: ['CodeFont', 'monospace'],
  },
}
```

### Add New Font Weight

```typescript
// tailwind.config.ts
{
  extend: {
    fontWeight: {
      'extra-bold': 800,
    },
  },
}
```

## Responsive Design

The theme uses Tailwind's responsive utilities:

```tsx
// Mobile-first approach
<div className="bg-surface p-4 md:p-6 lg:p-8">
  Responsive padding
</div>

// Hidden on mobile, shown on desktop
<div className="hidden md:block">
  Desktop-only content
</div>
```

## Animations & Transitions

### Transition Duration

```tsx
// Fast transition (100ms)
<button className="transition-all duration-100 hover:bg-surface-hover">
  Quick hover
</button>

// Standard transition (150ms)
<button className="transition-colors duration-150 hover:bg-surface-hover">
  Standard hover
</button>

// Slow transition (300ms)
<button className="transition-all duration-300 hover:bg-surface-hover">
  Slow hover
</button>
```

### Pulse Animation

```tsx
// For recording indicator
<div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
```

## Testing Your Customizations

### 1. Update `tailwind.config.ts`

```typescript
// tailwind.config.ts
{
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Your custom colors
      },
      fontFamily: {
        // Your custom fonts
      },
    },
  },
}
```

### 2. Restart Development Server

```bash
# Stop the server and restart
npm run dev
```

### 3. Test All Components

- Login/Register pages
- Chat interface
- Session list
- Modals and dialogs
- Voice controls
- File upload

### 4. Verify Accessibility

- Check color contrast ratios (minimum 4.5:1 for normal text)
- Test focus states on all interactive elements
- Ensure text is readable on all backgrounds

## Accessibility Considerations

### Color Contrast Ratio

All text colors meet WCAG AA standards:
- `#ffffff` on `#1a1a1a`: 15.2:1 (AAA)
- `#a1a1aa` on `#0f0f0f`: 9.9:1 (AAA)
- `#6366f1` on `##ffffff`: 4.5:1 (AA)

### Focus States

All interactive elements have visible focus states:
- `focus:outline-none focus:border-primary` for inputs
- `focus:ring-2 focus:ring-primary` for buttons

### Semantic HTML

Use proper semantic HTML:
- `<button>` for actions
- `<a>` for links
- `<label>` for form inputs

## Dark Mode Best Practices

### 1. Avoid Pure Black

Use `#0f0f0f` instead of `#000000` for the background to reduce harsh contrast.

### 2. Use Slightly Off-White

Use `#ffffff` for headings and `#a1a1aa` for body text instead of pure white everywhere.

### 3. Layer Colors

Create depth by using multiple shades:
```
Background (deepest) → Surface → Surface Hover → Primary
```

### 4. Add Subtle Borders

Borders help define boundaries between elements:
```tsx
<span className="border border-border">Bordered element</span>
```

## Example: Complete Component with Custom Theme

```tsx
function CustomCard({ title, children, action }) {
  return (
    <div className="bg-surface border border-border rounded-lg p-6 shadow-lg">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-text-primary text-xl font-semibold">
          {title}
        </h3>
        {action && (
          <button
            onClick={action.onClick}
            className="bg-primary hover:bg-primary-hover text-white px-3 py-1 rounded-md transition-colors duration-150 text-sm"
          >
            {action.label}
          </button>
        )}
      </div>
      <div className="text-text-secondary">
        {children}
      </div>
    </div>
  );
}
```

## Resources

- [Tailwind CSS Customization](https://tailwindcss.com/docs/customizing-colors)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Dark Mode UI Best Practices](https://www.smashingmagazine.com/2020/04/designing-for-dark-mode/)

For questions or suggestions about the theme, please open an issue on GitHub.
