---
sidebar_position: 3
title: "ROS 2 Fundamentals"
---

import TextbookToolbar from '@site/src/components/TextbookToolbar';

<TextbookToolbar />

# ROS 2 Fundamentals

## Introduction to ROS 2

Robot Operating System 2 (ROS 2) is a flexible framework for writing robot software. It's a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robot platforms.

## Architecture

### DDS-Based Communication

ROS 2 uses Data Distribution Service (DDS) as its middleware, providing:

- **Real-time performance**: Guaranteed message delivery within time constraints
- **Reliability**: Robust communication between nodes
- **Scalability**: Support for distributed systems
- **Security**: Built-in security features

### Nodes and Communication

#### Nodes

In ROS 2, a node is a process that performs computation. Nodes are organized in a graph and communicate with each other using:

- **Topics**: Publish/subscribe communication pattern
- **Services**: Request/response communication pattern
- **Actions**: Goal/cancel/feedback communication pattern

#### Communication Patterns

**Topics** enable asynchronous communication where publishers send messages to subscribers through a topic name.

**Services** provide synchronous request/response communication.

**Actions** are for long-running tasks that require feedback and the ability to cancel.

## Key Concepts

### Packages

ROS 2 organizes code into packages that contain:

- Source code
- Launch files
- Configuration files
- Dependencies
- Documentation

### Launch Files

Launch files allow you to start multiple nodes with a single command. They can be written in Python or XML.

### Parameters

Parameters in ROS 2 are used to configure nodes at runtime. They can be set at startup or changed dynamically.

## Installation and Setup

### System Requirements

ROS 2 supports multiple platforms:

- Ubuntu Linux (recommended)
- Windows
- macOS
- Real-time systems

### Installation Process

1. Add the ROS 2 repository to your system
2. Install ROS 2 packages
3. Source the ROS 2 environment
4. Verify installation with demos

## Core Tools

### Command Line Tools

ROS 2 provides various command-line tools:

- `ros2 run`: Run a node
- `ros2 launch`: Launch multiple nodes
- `ros2 topic`: Work with topics
- `ros2 service`: Work with services
- `ros2 action`: Work with actions
- `ros2 param`: Work with parameters

### Visualization Tools

- **RViz2**: 3D visualization tool for displaying robot state and sensor data
- **rqt**: Graphical user interface framework
- **ros2 bag**: Data recording and playback

## Programming with ROS 2

### Client Libraries

ROS 2 supports multiple programming languages:

- **rclcpp**: C++ client library
- **rclpy**: Python client library
- **rclnodejs**: Node.js client library
- **rclc**: C client library for embedded systems

### Creating a Package

To create a new package:

```bash
ros2 pkg create --build-type ament_cmake <package_name>
```

### Creating Nodes

Nodes are created by inheriting from the Node class in your chosen client library and implementing the desired functionality.

## Quality of Service (QoS)

QoS settings allow you to control how messages are delivered:

- **Reliability**: Best effort or reliable delivery
- **Durability**: Volatile or transient local durability
- **History**: Keep last N messages or keep all messages
- **Deadline**: Maximum time between messages

## Security

ROS 2 includes security features:

- **Authentication**: Verify node identity
- **Authorization**: Control what nodes can do
- **Encryption**: Encrypt communications

## Best Practices

- Use composition for better performance
- Implement proper error handling
- Use parameters for configuration
- Follow naming conventions
- Write tests for your nodes
- Document your code properly

## Migration from ROS 1

ROS 2 addresses many limitations of ROS 1:

- Real-time support
- Multi-robot systems
- Cross-platform compatibility
- Improved security
- Better build system