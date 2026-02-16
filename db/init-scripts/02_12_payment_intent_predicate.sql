\c app

CREATE OR REPLACE FUNCTION app_fcn.create_payment_intent(
    p_user_id uuid,
    p_session_id uuid,
    p_provider text,
    p_provider_intent_id text,
    p_status text,
    p_amount_cents integer,
    p_credit_applied_cents integer,
    p_currency text
)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = app, app_fcn, pg_temp
AS $$
	BEGIN
	    IF NOT app_fcn.is_self(p_user_id) THEN
	        RAISE EXCEPTION 'permission denied'
	            USING ERRCODE = 'AP401';
	    END IF;
	
	    IF NOT app_fcn.session_exists(p_session_id) THEN
	        RAISE EXCEPTION 'session not found'
	            USING ERRCODE = 'AP404';
	    END IF;
	
	    IF EXISTS (
	        SELECT 1
	        FROM app.payment_intent
	        WHERE session_id = p_session_id
	          AND user_id = p_user_id
	          AND status NOT IN ('canceled', 'failed')
	    ) THEN
	        RAISE EXCEPTION 'payment intent already exists'
	            USING ERRCODE = 'AP409';
	    END IF;
	
	    INSERT INTO app.payment_intent (
	        user_id,
	        session_id,
	        provider,
	        provider_intent_id,
	        status,
	        amount_cents,
	        credit_applied_cents,
	        currency,
	        created_at
	    ) VALUES (
	        p_user_id,
	        p_session_id,
	        p_provider,
	        p_provider_intent_id,
	        p_status,
	        p_amount_cents,
	        p_credit_applied_cents,
	        p_currency,
	        now()
	    );
	END;
$$;
