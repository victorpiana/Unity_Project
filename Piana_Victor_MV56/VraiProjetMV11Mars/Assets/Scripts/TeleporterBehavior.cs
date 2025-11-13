using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

public class TeleporterBehavior : MonoBehaviour
{
    private LineRenderer lineRenderer;
    private bool canTeleport = false;
    private bool pointerVisible = false;
    private Vector3 destinationPoint;

    public float maxDistance = 5f; // Distance max du rayon
    public string floorTag = "Floor"; // Tag à utiliser sur le sol
    public GameObject player; // XR Origin

    public Material validMaterial;   // 🟢 Matériau pour téléportation valide
    public Material invalidMaterial; // 🔴 Matériau pour téléportation invalide

    void Start()
    {
        lineRenderer = GetComponent<LineRenderer>();
        HidePointer();
    }

    void FixedUpdate()
    {
        if (pointerVisible)
        {
            lineRenderer.SetPosition(0, transform.position);
            RaycastHit hit;

            if (Physics.Raycast(transform.position, transform.TransformDirection(Vector3.forward), out hit, maxDistance))
            {
                lineRenderer.SetPosition(1, transform.position + transform.forward * hit.distance);

                // 🔄 Nouvelle logique : téléportation contrainte via script
                TeleportAnchor anchor = hit.collider.GetComponentInParent<TeleportAnchor>();

                if (anchor != null)
                {
                    canTeleport = true;
                    destinationPoint = anchor.GetTeleportPosition();
                    lineRenderer.material = validMaterial;
                }
                else if (hit.collider.gameObject.CompareTag(floorTag))
                {
                    canTeleport = true;
                    destinationPoint = hit.point;
                    lineRenderer.material = validMaterial;
                }
                else
                {
                    canTeleport = false;
                    lineRenderer.material = invalidMaterial;
                }
            }
            else
            {
                lineRenderer.SetPosition(1, transform.position + transform.forward * maxDistance);
                canTeleport = false;
                lineRenderer.material = invalidMaterial;
            }
        }
    }

    void ShowPointer()
    {
        if (lineRenderer != null)
        {
            lineRenderer.enabled = true;
        }
        pointerVisible = true;
    }

    void HidePointer()
    {
        if (lineRenderer != null)
        {
            lineRenderer.enabled = false;
        }
        pointerVisible = false;
    }

    void Teleport()
    {
        if (player != null)
        {
            player.transform.position = destinationPoint;
        }
    }

    public void OnTeleportAction(InputAction.CallbackContext context)
    {
        if (context.started)
        {
            ShowPointer();
        }

        if (context.canceled)
        {
            if (canTeleport)
            {
                Teleport();
            }
            HidePointer();
        }
    }
}
