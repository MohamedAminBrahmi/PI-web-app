import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  heroHighlights = [
    { value: '1,200+', label: 'Scouts Served', icon: '👥' },
    { value: '85+', label: 'Activities Tracked', icon: '🏕️' },
    { value: '24', label: 'Scout Units', icon: '🏠' }
  ];

  quickActions = [
    {
      icon: '📊',
      title: 'Plan Your Activity',
      description: 'Enter your activity details and get an estimate of how many scouts will attend.',
      route: '/prediction',
      accent: 'primary'
    },
    {
      icon: '🔮',
      title: 'Future Trends',
      description: 'See what participation looks like in the coming months to plan ahead.',
      route: '/forecasting',
      accent: 'blue'
    },
    {
      icon: '🎯',
      title: 'Who Will Attend?',
      description: 'Understand which scouts are likely to be active or less active in events.',
      route: '/classification',
      accent: 'green'
    },
    {
      icon: '📈',
      title: 'How Many Participants?',
      description: 'See how accurate our attendance estimates are based on past activities.',
      route: '/regression',
      accent: 'orange'
    },
    {
      icon: '👥',
      title: 'Compare Scout Units',
      description: 'See how different scout units are grouped and compare their activity levels.',
      route: '/clustering',
      accent: 'purple'
    },
    {
      icon: '📋',
      title: 'Overview',
      description: 'View a summary of all data and statistics across the association.',
      route: '/overview',
      accent: 'neutral'
    }
  ];

  howItWorks = [
    {
      step: '1',
      icon: '📝',
      title: 'Enter Your Details',
      description: 'Tell us about your planned activity — type, duration, budget, season, and target age group.'
    },
    {
      step: '2',
      icon: '🤖',
      title: 'Get an Estimate',
      description: 'Our system analyzes past activities to predict how many scouts will participate.'
    },
    {
      step: '3',
      icon: '✅',
      title: 'Plan With Confidence',
      description: 'Use the estimate to prepare the right amount of supplies, transport, and leaders.'
    }
  ];

  testimonials = [
    {
      quote: 'Now I know exactly how many meals to prepare for our camping trips.',
      author: 'Scout Leader',
      role: 'Tunis Region'
    },
    {
      quote: 'The activity planner saved us from over-booking transport twice already.',
      author: 'Unit Coordinator',
      role: 'Sousse Region'
    }
  ];

  constructor() { }

  ngOnInit(): void {
  }
}
