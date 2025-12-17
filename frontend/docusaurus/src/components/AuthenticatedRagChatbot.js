import React from 'react';
import { AuthProvider } from './AuthProvider';
import RagChatbot from './RagChatbot';

// AuthenticatedRagChatbot: A wrapper that ensures RagChatbot has access to AuthProvider
const AuthenticatedRagChatbot = (props) => {
  return (
    <AuthProvider>
      <RagChatbot {...props} />
    </AuthProvider>
  );
};

export default AuthenticatedRagChatbot;